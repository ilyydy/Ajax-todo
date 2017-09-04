// TODO API
// 获取 blog
var apiBlogDetail = function(callback) {
    var path = '/api/blog/detail' + window.location.search
    ajax('GET', path, '', callback)
}

var apiBlogCommentAll = function(callback) {
    var path = '/api/blogComment/all'
    ajax('GET', path, '', callback)
}

var apiBlogCommentAdd = function(form, callback) {
    var path = '/api/blogComment/add'
    ajax('POST', path, form, callback)
}

var apiBlogCommentDelete = function(id, callback) {
    var path = '/api/blogComment/delete?id=' + id
    ajax('GET', path, '', callback)
}

var blogTemplate = function(blog) {
    var title = blog.title
    var content = blog.content
    var author = blog.author
    var id = blog.id
    //var w_user_id = weibo.user_id
    // data-* 是 HTML5 新增的自定义标签属性的方法
    // data-id="1" 获取属性的方式是 .dataset.id
    var t = `
        <div class="bolg-cell" data-blog_id="${id}">
            <h1 id="id-blog-title" class="center">${title}</h1>
            <h3 id='id-blog-author' class="center">${author}</h3>
            <div id="id-blog-content" class="markdown-body">${content}</div>
        </div>
    `
    return t
}

var blogCommentTemplate = function(blogComment) {
    var bc_content = blogComment.content
    var bc_id = blogComment.id
    //var c_user_id = comment.user_id
    var t = `
    <div class="blogComment-cell" data-blogcomment_id="${bc_id}">
    <span class="blogComment-content markdown-body">${bc_content}</span>
    <button class="blogComment-delete" data-blogcomment_id="${bc_id}">删除</button>
    </div>`
    return t
}

var insertBlog = function(blog) {
    var blogCell = blogTemplate(blog)
    var blogList = e('.blog-list')
    blogList.insertAdjacentHTML('beforeend', blogCell)
}

var insertBlogComment = function(blogComment) {
    var blogCommentCell = blogCommentTemplate(blogComment)
    var blogCommentList = e('#blogComment-list')
    blogCommentList.insertAdjacentHTML('afterBegin', blogCommentCell)
    e('#id-input-blogComment-content').value =''
}

// TODO DOM
var loadBlog = function() {
    // 调用 ajax api 来载入数据
    apiBlogDetail(function(r) {
        console.log('load blog', r)
        // 解析为 数组
        var blog = JSON.parse(r)
        insertBlog(blog)
    })

    apiBlogCommentAll(function(r) {
        log('开始解析blogComments')
        var blogComments = JSON.parse(r)
        log('返回的blogComments', blogComments)
        // 循环添加到页面中
        for(var i = 0; i < blogComments.length; i++) {
            var blogComment = blogComments[i]
            insertBlogComment(blogComment)
        }
    })
}

var bindEventBlogCommentAdd = function() {
    var b = e('#id-button-blogComment-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-blogComment-content')
        var content = input.value
        var blogCell = e('.bolg-cell')
        var blog_id = blogCell.dataset.blog_id
        log('click add', content)
        var form = {
            content: content,
            blog_id: blog_id,
        }
        log('form', form)
        apiBlogCommentAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var blogComment = JSON.parse(r)
            insertBlogComment(blogComment)
        })
    })
}

var bindEventBlogCommentDelete = function() {
    var blogCommentList = e('#blogComment-list')
    blogCommentList.addEventListener('click', function(event){
        log(event)
        var self = event.target
        log(self.classList)
        if (self.classList.contains('blogComment-delete')) {
            log('点到了 评论删除按钮')
            var blogCommentId = self.dataset.blogcomment_id
            log('blogCommentId', blogCommentId)
            apiBlogCommentDelete(blogCommentId, function(r) {
                log('服务器响应删除成功', r)
                // 收到返回的数据, 删除 self 的父节点
                self.parentElement.remove()
            })
          }
      })

}

var bindEvents = function() {
    bindEventBlogCommentAdd()
    bindEventBlogCommentDelete()
}


var __main = function() {
    bindEvents()
    loadBlog()
}

__main()
