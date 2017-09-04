
// WEIBO API
// 获取所有 weibo
var apiWeiboAll = function(callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}

// 增加一个 weibo
var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}

// 删除一个 weibo
var apiWeiboDelete = function(id, callback) {
    var path = '/api/weibo/delete?id=' + id
    ajax('GET', path, '', callback)
}

var apiCommentAll = function(callback) {
    var path = '/api/comment/all'
    ajax('GET', path, '', callback)
}

var apiCommentAdd = function(form, callback) {
    var path = '/api/comment/add'
    ajax('POST', path, form, callback)
}

var apiCommentDelete = function(id, callback) {
    var path = '/api/comment/delete?id=' + id
    ajax('GET', path, '', callback)
}
// weibo DOM
var WeiboTemplate = function(weibo) {
    var w_content = weibo.content
    var w_id = weibo.id
    //var w_user_id = weibo.user_id
    // data-* 是 HTML5 新增的自定义标签属性的方法
    // data-id="1" 获取属性的方式是 .dataset.id
    var t = `
        <div class="weibo-cell" data-weibo_id="${w_id}">
            <button class="weibo-delete" data-weibo_id="${w_id}">删除</button>
            <button class="comment-add-button" data-weibo_id="${w_id}">增加评论</button>
            <span class="weibo-content">${w_content}</span>
        </div>
    `
    return t
}

var CommentTemplate = function(comment) {
    var c_content = comment.content
    var c_id = comment.id
    //var c_user_id = comment.user_id
    var t = `
        <div class="comment-cell" data-comment_id="${c_id}">
            <button class="comment-delete" data-comment_id="${c_id}">删除</button>
            <span class="comment-content">${c_content}</span>
        </div>`
    return t
}

var CommentAddFormTemplate = function() {
    var t = `
      <div class="comment-add-form">
        <input class="comment-add-input">
        <button class="comment-add">确定</button>
      </div>
    `
    return t
}

var insertWeibo = function(weibo) {
    // var content = weibo['content']
    // var content = weibo.content
    var weiboCell = WeiboTemplate(weibo)
    // 插入 weibo-list
    var weiboList = e('#weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

var insertComment = function(comment, weiboCell) {
    // var content = comment['content']
    // var content = comment.content
    var commentCell = CommentTemplate(comment)
    weiboCell.insertAdjacentHTML('beforeend', commentCell)
}

var loadWeibos = function() {
    // 调用 ajax api 来载入数据
    apiWeiboAll(function(r) {
        console.log('load all', r)
        // 解析为 数组
        var weibos = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo)
        }
    })
    log('weibo结束')
    // 开始插入评论
    apiCommentAll(function(r) {
        log('开始解析comments')
        var comments = JSON.parse(r)
        log('返回的comments', comments)
        // 循环添加到页面中
        for(var i = 0; i < comments.length; i++) {
            var comment = comments[i]
            var weiboId = comment.weibo_id
            var w = `.weibo-cell[data-weibo_id="${weiboId}"]`
            var weiboCell = document.querySelector(w)
            insertComment(comment, weiboCell)
        }
    })
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        log('form', form)
        apiWeiboAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var weibo = JSON.parse(r)
            insertWeibo(weibo)
        })
    })
}

var bindEventWeiboDelete = function() {
    var weiboList = e('#weibo-list')
    log(weiboList)
    weiboList.addEventListener('click', function(event){
        log(event)
        // 通过 event.target 来得到被点击的对象
        var self = event.target
        // 通过比较被点击元素的 class 来判断元素是否是想要的
        // classList 属性保存了元素所有的 class
        log(self.classList)
        if (self.classList.contains('weibo-delete')) {
            log('点到了 删除按钮')
            var weiboId = self.dataset.weibo_id
            apiWeiboDelete(weiboId, function(r) {
                log('服务器响应删除微博成功', r)
                // 收到返回的数据, 删除 self 的父节点
                self.parentElement.remove();
            })
          }
      })

}

var bindEventCommentAddBox = function() {
    var weiboList = e('#weibo-list')
    weiboList.addEventListener('click', function(event){
        log(event)
        var self = event.target
        log(self.classList)
        if (self.classList.contains('comment-add-button')) {
            log('点到了 新增按钮')
            var t = CommentAddFormTemplate()
            var weibo_cell = self.closest('.weibo-cell')
            weibo_cell.insertAdjacentHTML('beforeend', t)
          }
      })

}

var bindEventCommentAdd = function() {
    var weiboList = e('#weibo-list')
    log(weiboList)
    weiboList.addEventListener('click', function(event){
        log(event)
        // 通过 event.target 来得到被点击的对象
        var self = event.target

        if (self.classList.contains('comment-add')) {
          var weiboCell = self.closest('.weibo-cell')
          var input = weiboCell.querySelector('.comment-add-input')
          var weibo_id = weiboCell.dataset.weibo_id
          var form = {
            weibo_id: weibo_id,
            content: input.value,
          }
          log('update form', form)
          apiCommentAdd(form, function(r) {
              log('add', r)
              var c_addForm = weiboCell.querySelector('.comment-add-form')
              c_addForm.remove()
              var comment = JSON.parse(r)
              insertComment(comment, weiboCell)
          })
      }
    })
}

var bindEventCommentDelete = function() {
    var weiboList = e('#weibo-list')
    weiboList.addEventListener('click', function(event){
        log(event)
        var self = event.target
        log(self.classList)
        if (self.classList.contains('comment-delete')) {
            log('点到了 评论删除按钮')
            var commentId = self.dataset.comment_id
            apiCommentDelete(commentId, function(r) {
                log('服务器响应删除成功', r)
                // 收到返回的数据, 删除 self 的父节点
                self.parentElement.remove()
            })
          }
      })

}

var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventCommentAddBox()
    bindEventCommentAdd()
    bindEventCommentDelete()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
