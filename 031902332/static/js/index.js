$(document).ready(function(){
    //初始化系统信息
    var $container = document.getElementById('container');
    // 初始化牌堆
    var deck = Deck();
    // 绑定标签
    deck.mount($container);
    // 牌堆牌面翻转
    deck.flip();
    // 牌堆出现效果
    deck.intro();
    // 加载背景音乐，循环执行
    background_index();
    setInterval(background_index, 154 * 1000);

    // 加载背景音乐
    function background_index(){
        let playerc = $("#jplayer");
        if (playerc.data().jPlayer && playerc.data().jPlayer.internal.ready === true) {
            playerc.jPlayer("setMedia", {
                mp3: "static/static/background_index.mp3"
            }).jPlayer("play");//jPlayer("play") 用来自动播放
        }else {
            playerc.jPlayer({
                ready: function() {
                    $(this).jPlayer("setMedia", {
                        mp3: "static/static/background_index.mp3" //同上
                    }).jPlayer("play");//同上
                },
                swfPath: "static/node_modules/jPlayer/dist/jplayer/jquery.jplayer.swf",
                supplied: "mp3"
            });
        }
    }
});