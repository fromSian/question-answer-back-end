# 启动项目

```bash
python manage.py runserver
```

see: http://localhost:8000/

swagger: http://localhost:8000/swagger/

后台管理: http://localhost:8000/admin/

# 创建超级管理员

```bash
python manage.py createsuperuser
```

用户名和密码必须填，其他可选

当前数据库超管：admin/123456

# 数据库迁移

在修改了 models 或初始化创建数据库时执行命令

```bash
python manage.py makemigrations
python manage.py migrate
```

# 前台用户管理

- 通过前台注册的用户所属于【普通用户】组，没有权限登录到后台管理系统。
- 只有所属于【普通用户】组的用户，可以成功登录前台系统。超级管理员或举报审核用户或其他自定义组用户都无法登录前台系统

# 举报审核

- 在后台管理-组中添加【举报审核】用户组，并赋权【Denounce ｜ denounce ｜ can change denounce】（有权限修改 denounce 记录）。创建一个属于【举报审核】组的用户。
  (当前数据库中已有, 举报审核用户为 audit/Lx123456)

- 使用举报审核用户登录后台管理系统，修改 debounce【状态】一列。

# 金币+免费发布提问次数设计

- 用户注册时金币数为 0，免费发布提问次数为 2.
- 每月 1 日，所有用户免费发布提问次数更新为 2.
- 发布提问时，若用户免费发布提问次数不为 0，则发布一次提问，次数减一。若免费发布提问次数为 0，金币数大于等于 2，则发布一次提问，金币数减 2.若免费发布提问次数为 0，金币数小于 2，则该用户暂时无法发布提问。
- 当举报(debounce)记录被更新为【通过】时，这条记录关联的发起举报用户金币数+2。
- 当一条作答被标记为【优秀作答】时，这条作答的发出用户金币数+2。
