// TODO API
// 获取所有 blog
var apiBlogAll = function(callback) {
    var path = '/api/blog/all'
    ajax('GET', path, '', callback)
}

// 删除一个 blog
var apiBlogDelete = function(id, callback) {
    var path = '/api/blog/delete?id=' + id
    ajax('GET', path, '', callback)
}

// TODO DOM
var blogTemplate = function(blog) {
    var title = blog.title
    var id = blog.id
    var updated_time = timeString(blog.updated_time)
    // data-* 是 HTML5 新增的自定义标签属性的方法
    // data-id="1" 获取属性的方式是 .dataset.id
    var t = `
        <tr class="blog-cell" data-id="${id}">
            <td>
            <a href="/blog/detail?id=${id}" class="blog-title">${title}</a>
            </td>
            <td>
            <span>${updated_time}</span>
            </td>
            <td>
            <button class="blog-delete" data-id="${id}">删除</button>
            </td>
            <td>
            <button onclick="location.href='/api/blog/edit?id=${id}'">编辑</button>
        </tr>
    `
    return t
}

var insertBlog = function(blog) {
    var blogCell = blogTemplate(blog)
    // 插入 blog-list
    var blogList = e('#id-blog-list')
    blogList.insertAdjacentHTML('beforeend', blogCell)
}

var loadBlogs = function() {
    // 调用 ajax api 来载入数据
    apiBlogAll(function(r) {
        console.log('load all', r)
        // 解析为 数组
        var blogs = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < blogs.length; i++) {
            var blog = blogs[i]
            insertBlog(blog)
        }
    })
}

var bindEventBlogDelete = function() {
    var blogList = e('#id-blog-list')
    log(blogList)
    blogList.addEventListener('click', function(event){
        log(event)
        // 通过 event.target 来得到被点击的对象
        var self = event.target
        // 通过比较被点击元素的 class 来判断元素是否是想要的
        // classList 属性保存了元素所有的 class
        log(self.classList)
        if (self.classList.contains('blog-delete')) {
            log('点到了 删除按钮')
            var blogId = self.dataset.id
            apiBlogDelete(blogId, function(r) {
                log('服务器响应删除成功', r)
                // 收到返回的数据, 删除 self 的父节点
                self.closest('.blog-cell').remove()
            })
          }
      })

}

var bindEvents = function() {
    bindEventBlogDelete()
}

var __main = function() {
    bindEvents()
    loadBlogs()
}

__main()
