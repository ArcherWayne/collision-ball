# to do list
1. ball的碰撞还有问题, ball的碰撞应该和player的不一样
   1. 添加方向向量反向即可
2. player的边界检测还有问题
   1. 不能直接用pos和rect更新, 要分别使用pos.x和pos.y
3. player和ball之间没有碰撞, 怎么回事?
   1. 完成 要将player的位置也传给ball, 并且在碰撞检测中增加player的rect


# collision balls to do list
1. 这个需要delta time
2. 用drawio画个概念图
3. 研究下group的概念