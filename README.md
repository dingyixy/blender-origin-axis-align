# Blender Origin Axis Alignment

**Blender 原点轴向对齐工具 | Copy local axis orientation while keeping geometry in place**

## 中文介绍

一个轻量级 Blender Python 脚本，用于将多个目标物体的局部坐标轴方向对齐到活动物体。脚本提取参考物体的世界空间旋转，并通过反向补偿目标的底层几何数据，使普通静态网格的基础几何体在世界空间中保持原位。

它复制的是原点的轴向，不会把目标原点移动到源物体的位置。适合需要统一模型局部坐标方向，以便后续进行局部移动、旋转和缩放的工作流程。

### 主要功能

- **批量对齐**：将多个目标物体的轴向对齐到同一个参考物体。
- **几何补偿**：调整物体旋转时，同步补偿底层几何数据，保持基础几何体的世界空间位置。
- **保留目标位置和缩放分量**：构建新世界矩阵时，保留目标原世界矩阵分解得到的位置和缩放。
- **共享数据保护**：修改前为多用户共享数据创建独立副本，避免直接影响其他共享该数据的物体。
- **控制台反馈**：输出成功、跳过或选择不足的提示。

### 使用方法

1. 在 Blender 中切换到 **物体模式（Object Mode）**。
2. 先选中一个或多个需要调整轴向的目标物体。
3. 最后按住 **Shift** 选中参考物体，使其成为**活动物体**。
4. 在 **Scripting** 工作区的文本编辑器中打开 `复制原点轴向.py`。
5. 点击 **Run Script** 运行脚本。
6. 将变换方向切换为 **Local**，检查对齐后的局部坐标轴。

至少需要选中两个物体。活动物体作为源物体，其余选中物体作为目标。源物体不会被修改。

### 工作原理

脚本使用源物体的世界旋转，以及目标物体原有的位置和分解后的缩放，构造新的世界矩阵，再计算几何补偿矩阵：

```text
补偿矩阵 = 新世界矩阵的逆矩阵 × 原世界矩阵
新世界矩阵 × 补偿矩阵 × 原顶点 = 原世界矩阵 × 原顶点
```

因此，在普通静态网格等适用条件下，基础几何体的世界空间位置保持不变，而物体的局部轴向得到调整。

### 注意事项与当前限制

- 当前版本是独立运行的脚本，没有插件注册入口、面板或自定义操作按钮。
- 建议优先用于普通静态网格，运行前保存文件或备份对象。脚本会实际修改底层几何数据。
- 脚本根据数据是否具有 `transform` 方法筛选目标；这不代表所有通过检查的数据类型均已验证，末尾的 `data.update()` 调用也需要类型兼容。
- 共享数据会变为独立副本，因此目标原有的关联复制关系可能被解除。
- 修改器、约束、父子层级、动画、形态键、负缩放和剪切没有专门处理，最终显示结果需要单独验证。子物体没有世界变换补偿逻辑。
- 零缩放等不可逆变换可能导致矩阵求逆失败；当前没有逐对象异常恢复机制。
- 尚未声明或实测 Blender 兼容版本。

---

## English

### Overview

A lightweight Blender Python script that aligns the local axes of multiple target objects to an active reference object. It extracts the reference object's world-space rotation and counter-transforms each target's underlying geometry to keep ordinary static mesh geometry in place in world space.

The script copies origin orientation, not origin position. It is useful for standardizing local axis directions before further local-space translation, rotation, and scaling.

### Features

- **Batch alignment:** Align multiple targets to one reference object.
- **Geometry compensation:** Counter-transform the underlying geometry when changing object rotation to preserve base geometry positions in world space.
- **Preserved target translation and scale components:** Build the new world matrix using the translation and scale decomposed from the target's original world matrix.
- **Shared-data protection:** Create an independent copy of multi-user data before editing to avoid directly affecting other objects sharing that data.
- **Console feedback:** Report successful operations, skipped objects, and insufficient selection.

### Usage

1. Switch to **Object Mode** in Blender.
2. Select one or more target objects whose local axes you want to adjust.
3. **Shift-select the reference object last**, making it the **active object**.
4. Open `复制原点轴向.py` in the Text Editor in the **Scripting** workspace.
5. Click **Run Script**.
6. Set the transform orientation to **Local** to inspect the aligned axes.

Select at least two objects. The active object is the source; all other selected objects are targets. The source remains unchanged.

### How It Works

The script combines the source's world-space rotation with the target's original translation and decomposed scale to build a new world matrix. It then calculates a geometry compensation matrix:

```text
compensation = inverse(new_world_matrix) × original_world_matrix
new_world_matrix × compensation × original_vertex
= original_world_matrix × original_vertex
```

Under suitable conditions, such as ordinary static meshes, base geometry stays in place in world space while the object's local axes change orientation.

### Notes and Limitations

- This is a standalone script with no add-on registration, panel, or custom operator.
- Intended primarily for ordinary static meshes. Save your file or back up objects before running it, as it modifies the underlying geometry data.
- Targets are filtered by the presence of a data-level `transform` method. This does not guarantee full support for every eligible data type; the final `data.update()` call must also be compatible.
- Shared data is made independent, which may break the target's existing linked-duplicate relationship.
- Modifiers, constraints, parenting, animation, shape keys, negative scale, and shear have no dedicated handling and require separate validation. Child objects receive no world-transform compensation.
- Non-invertible transforms, such as zero scale, may cause matrix inversion to fail. There is currently no per-object exception recovery.
- No Blender compatibility range has been declared or tested yet.
