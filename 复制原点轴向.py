import bpy
from mathutils import Matrix

def copy_origin_rotation():
    # 获取当前的上下文环境
    context = bpy.context
    active_obj = context.active_object
    selected_objs = context.selected_objects

    # 检查是否至少选中了两个物体
    if not active_obj or len(selected_objs) < 2:
        print("【错误】请至少选中两个物体！(先选目标物体，最后Shift加选源物体)")
        return

    # 最后选中的活动物体作为源物体 (A)
    source = active_obj
    # 其他被选中的物体作为目标物体 (B，支持同时选中多个目标)
    targets = [obj for obj in selected_objs if obj != source]

    # 从源物体的世界矩阵中拆解出：位置、旋转、缩放。我们只提取它的“旋转 (rot_A)”
    _, rot_A, _ = source.matrix_world.decompose()

    for target in targets:
        # 检查物体是否有数据层面的 transform 方法 (通常网格Mesh、曲线Curve支持)
        if not hasattr(target.data, "transform"):
            print(f"【跳过】物体 '{target.name}' 不支持数据层面的顶点变换。")
            continue

        # 如果目标物体的网格数据是多用户共享的（比如按Alt+D复制的），
        # 修改它会影响其他物体，所以先将其单用户化 (Make Single User)
        if target.data.users > 1:
            target.data = target.data.copy()

        # 获取目标物体 B 当前的世界矩阵
        W_B = target.matrix_world.copy()
        
        # 拆解出目标物体 B 的位置和缩放 (保持不变)
        loc_B, _, scale_B = W_B.decompose()

        # 组合出目标物体 B 的【新世界矩阵】 = (B的原有位置, A的旋转轴向, B的原有缩放)
        W_B_new = Matrix.LocRotScale(loc_B, rot_A, scale_B)

        # 计算网格数据需要补偿的差值矩阵：新矩阵的逆矩阵 乘以 旧矩阵
        # 这样能让顶点在世界空间中保持不动，抵消掉物体层面的旋转
        diff_mat = W_B_new.inverted() @ W_B

        # 将补偿矩阵直接应用到目标物体的底层网格数据上
        target.data.transform(diff_mat)

        # 最后，将目标物体的物理属性矩阵替换为我们刚刚算好的新矩阵
        target.matrix_world = W_B_new

        # 刷新物体的网格数据以在视图中显示更新
        target.data.update()
        
        print(f"【成功】已将 '{target.name}' 的原点轴向对齐至 '{source.name}'。")

# 运行函数
copy_origin_rotation()