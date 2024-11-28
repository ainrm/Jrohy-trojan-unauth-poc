# Jrohy/trojan Unauthorized modification of administrator password

[中文版本(Chinese version)](README.zh-cn.md)

Jrohy/trojan is an open source project based on Go to automatically deploy trojan services. Its web-side initialization interface `/auth/register` failed to close properly after user configuration, allowing unauthorized visitors to directly modify the administrator password.

Source Project:

- https://github.com/Jrohy/trojan

Affected versions:

- v2.0.0 - v2.15.3



## Vulnerability Principle

Register the route and use the `updateUser` function to handle `/auth/register` requests

```go
// https://github.com/Jrohy/trojan/blob/master/web/auth.go#L155

func Auth(r *gin.Engine, timeout int) *jwt.GinJWTMiddleware {
    jwtInit(timeout)

    newInstall := gin.H{"code": 201, "message": "No administrator account found inside the database", "data": nil}
    r.NoRoute(authMiddleware.MiddlewareFunc(), func(c *gin.Context) {
        claims := jwt.ExtractClaims(c)
        fmt.Printf("NoRoute claims: %#v\n", claims)
        c.JSON(404, gin.H{"code": 404, "message": "Page not found"})
    })
    ...
    r.POST("/auth/register", updateUser)
```

Extract `password` from the request and pass it to `SetValue`

```go
// https://github.com/Jrohy/trojan/blob/master/web/auth.go#L113

func updateUser(c *gin.Context) {
    responseBody := controller.ResponseBody{Msg: "success"}
    defer controller.TimeCost(time.Now(), &responseBody)
    username := c.DefaultPostForm("username", "admin")
    pass := c.PostForm("password")
    err := core.SetValue(fmt.Sprintf("%s_pass", username), pass)
    if err != nil {
        responseBody.Msg = err.Error()
    }
    c.JSON(200, responseBody)
}
```

Update the database and write the new password

```go
// https://github.com/Jrohy/trojan/blob/master/core/leveldb.go#L30

func SetValue(key string, value string) error {
    db, err := leveldb.OpenFile(dbPath, nil)
    if err != nil {
        return err
    }
    defer db.Close()
    return db.Put([]byte(key), []byte(value), nil)
}
```



## Proof of vulnerability

![20241127170540](./20241127170540.webp)
