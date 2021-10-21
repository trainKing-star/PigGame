$(document).ready(function(){
            let deck_container = init("container");
            let player1 = null, player2 = null;
            deck_container.shuffle();
            deck_container.fan();
            let record = 0, record_suit = null;
            let GAME = 0;

            $("#container .card").on("mouseenter", c_seen);
            $("#container .card").on("mouseleave", c_leave);
            $("#container .card").on("mouseup", mouseup);

            action_add("div.bgImg1.header.player1");
            background_game();

            setInterval(background_game, 40 * 1000);

            function background_game(){
                let playerc = $("#jplayer");
                if (playerc.data().jPlayer && playerc.data().jPlayer.internal.ready === true) {
                    playerc.jPlayer("setMedia", {
                        mp3: "static/background_game.mp3"
                    }).jPlayer("play");//jPlayer("play") 用来自动播放
                }else {
                    playerc.jPlayer({
                        ready: function() {
                            $(this).jPlayer("setMedia", {
                                mp3: "static/background_game.mp3" //同上
                            }).jPlayer("play");//同上
                        },
                        swfPath: "node_modules/jPlayer/dist/jplayer/jquery.jplayer.swf",
                        supplied: "mp3"  //acc属于M4A
                    });
                }
            }

            function background_get_p(){
                let playerc = $("#get_p");
                if (playerc.data().jPlayer && playerc.data().jPlayer.internal.ready === true) {
                    playerc.jPlayer("setMedia", {
                        mp3: "static/get_p.mp3"
                    }).jPlayer("play");//jPlayer("play") 用来自动播放
                }else {
                    playerc.jPlayer({
                        ready: function() {
                            $(this).jPlayer("setMedia", {
                                mp3: "static/get_p.mp3" //同上
                            }).jPlayer("play");//同上
                        },
                        swfPath: "node_modules/jPlayer/dist/jplayer/jquery.jplayer.swf",
                        supplied: "mp3"  //acc属于M4A
                    });
                }
            }

            function background_get_success(){
                let playerc = $("#get_success");
                if (playerc.data().jPlayer && playerc.data().jPlayer.internal.ready === true) {
                    playerc.jPlayer("setMedia", {
                        mp3: "static/get_success.mp3"
                    }).jPlayer("play");//jPlayer("play") 用来自动播放
                }else {
                    playerc.jPlayer({
                        ready: function() {
                            $(this).jPlayer("setMedia", {
                                mp3: "static/get_success.mp3" //同上
                            }).jPlayer("play");//同上
                        },
                        swfPath: "node_modules/jPlayer/dist/jplayer/jquery.jplayer.swf",
                        supplied: "mp3"  //acc属于M4A
                    });
                }
            }

            function background_move(){
                let playerc = $("#move");
                if (playerc.data().jPlayer && playerc.data().jPlayer.internal.ready === true) {
                    playerc.jPlayer("setMedia", {
                        mp3: "static/move.mp3"
                    }).jPlayer("play");//jPlayer("play") 用来自动播放
                }else {
                    playerc.jPlayer({
                        ready: function() {
                            $(this).jPlayer("setMedia", {
                                mp3: "static/move.mp3" //同上
                            }).jPlayer("play");//同上
                        },
                        swfPath: "node_modules/jPlayer/dist/jplayer/jquery.jplayer.swf",
                        supplied: "mp3"  //acc属于M4A
                    });
                }
            }

            function action_add(string) {
                $(string).addClass("big");
            }

            function action_remove(string) {
                $(string).removeClass("big");
            }

            let c_click = 0;
            function c_seen(card){
                c_click = 1;
                let vw = $(window).width();
                let origin = card.currentTarget.style.transform;
                card.currentTarget.style["z-index"] = parseInt(card.currentTarget.style["z-index"]) + 200;
                card.currentTarget.style.transform = origin + "perspective(" + vw * 0.8 + "px) translateZ(" + vw * 0.10 + "px)";
            }

            function c_leave(card){
                if(!c_click) return;
                let origin = card.currentTarget.style.transform.split(" ");
                origin = origin.slice(0, origin.length - 2).join(" ");
                card.currentTarget.style["z-index"] = parseInt(card.currentTarget.style["z-index"]) - 200;
                card.currentTarget.style.transform = origin;
            }



            function mouseup(card){
                if(!c_click) return;
                background_move();
                $("#container .card").off("mouseenter");
                $("#container .card").off("mouseleave");
                $("#container .card").off("mouseup");

                let t = $(this);

                deck_container.cards.forEach(function (card){
                    if(card.$el.style["z-index"] === t.css("z-index")){
                        card.setSide('front');
                    }
                });

                $(this).attr("id", "show");
                function f() {
                    let end = 1;
                    deck_container.cards.forEach(function (card){
                        if(card.$el.className === "card")  {
                            end = 0;
                            return true;
                        }
                        if(card.$el.style["z-index"] >= 200){
                            if(record_suit==null) record_suit = card;
                            else if(card.i !== record_suit.i && card.suit === record_suit.suit){
                                if(GAME === 0) player1 = player_one_init("player1");
                                else player2 = player_one_init("player2");
                                record_suit = null;
                            }
                            else record_suit = card;
                            return false;
                        }
                    });
                    if(end === 1) {
                        $(".end").css("display", "");
                        let p1 = 0;
                        player1.cards.forEach(function (card){
                            if(card.$root != null) p1++;
                        });
                        let p2 = 0;
                        player2.cards.forEach(function (card){
                            if(card.$root != null) p2++;
                        });
                        $("p.text1").text(p1);
                        $("p.text2").text(p2);
                        function index() {
                            window.location.href = "index.html";
                        }
                        function s1() {
                            $(".success1").css("display", "");
                            $(".photo").css("display", "none");
                        }
                        function s2() {
                            $(".success2").css("display", "");
                            $(".photo").css("display", "none");
                        }
                        background_get_success();
                        if(p1>p2) setInterval(s2, 2000);
                        else if(p1<p2) setInterval(s1, 2000);
                        setInterval(index, 5000);
                        return;
                    }

                    card.currentTarget.style["z-index"] = record;
                    record++;
                    c_click = 0;
                    if (GAME === 0 ) {
                        GAME = 1;
                        $("#player1 .card").off("mousedown");
                        $("#player2 .card").on("mousedown", p2_mousedown);
                        action_add("div.bgImg2.footer.player2");
                        action_remove("div.bgImg1.header.player1");
                    }
                    else {
                        GAME = 0;
                        $("#player2 .card").off("mousedown");
                        $("#player1 .card").on("mousedown", p1_mousedown);
                        action_remove("div.bgImg2.footer.player2");
                        action_add("div.bgImg1.header.player1");
                    }

                    $("#container .card").on("mouseenter", c_seen);
                    $("#container .card").on("mouseleave", c_leave);
                    $("#container .card").on("mouseup", mouseup);
                    t.unbind();
                }
                setTimeout(f, 2000);
            }

            let click_f = 0;
            $("#footer").mousedown(function (){
                if(click_f === 0){
                    $("#player1").css({
                        "animation-name": "player1_change_end",
                        "animation-duration":"2s",
                        "animation-fill-mode":"forwards"
                    });
                    $("#container .card").off("mouseenter", c_seen);
                    $("#container .card").off("mouseleave", c_leave);
                    $("#container .card").off("mouseup", mouseup);
                    click_f = 1;
                }
                else if(click_f === 1){
                    $("#player1").css({
                        "animation-name": "player1_change_start",
                        "animation-duration":"2s",
                        "animation-fill-mode":"forwards"
                    });
                    click_f = 0;
                    $("#container .card").on("mouseenter", c_seen);
                    $("#container .card").on("mouseleave", c_leave);
                    $("#container .card").on("mouseup", mouseup);
                }
            });

            let click_h = 0;
            $("#header").mousedown(function (){
                if(click_h === 0){
                    $("#player2").css({
                        "animation-name": "player2_change_end",
                        "animation-duration":"2s",
                        "animation-fill-mode":"forwards"
                    });
                    click_h = 1;
                    $("#container .card").off("mouseenter", c_seen);
                    $("#container .card").off("mouseleave", c_leave);
                    $("#container .card").off("mouseup", mouseup);
                }
                else if(click_h === 1){
                    $("#player2").css({
                        "animation-name": "player2_change_start",
                        "animation-duration":"2s",
                        "animation-fill-mode":"forwards"
                    });
                    click_h = 0;
                    $("#container .card").on("mouseenter", c_seen);
                    $("#container .card").on("mouseleave", c_leave);
                    $("#container .card").on("mouseup", mouseup);
                }
            });


            function p1_mouseenter(card){
                let vw = $(window).width();
                let origin = card.currentTarget.style.transform;
                card.currentTarget.style["z-index"] = parseInt(card.currentTarget.style["z-index"]) + 200;
                card.currentTarget.style.transform = origin + "perspective(" + vw * 0.8 + "px) translateZ(" + vw * 0.10 + "px)";
                event.stopPropagation()
            }


            function p1_mouseleave(card){
                let origin = card.currentTarget.style.transform.split(" ");
                origin = origin.slice(0, origin.length - 2).join(" ");
                card.currentTarget.style["z-index"] = parseInt(card.currentTarget.style["z-index"]) - 200;
                card.currentTarget.style.transform = origin;
                event.stopPropagation()
            }

            let chick_mp1 = 0;
            function p1_mousedown(){
                if(GAME === 1 || chick_mp1 === 1) return;
                chick_mp1 = 1;
                background_move();
                let t = $(this);
                player1.cards.forEach(function (card) {
                    if (card.$el.className === t.attr("class")) {
                        card.unmount();
                        let label = null;
                        deck_container.cards.forEach(function (c) {
                            if(c.i === card.i){
                                label = c;
                                return false
                            }
                        });
                        label.mount($("#container .deck")[0]);
                        label.$el.style["z-index"] = parseInt(label.$el.style["z-index"]) + 200;
                        function f() {
                            let end = 1;
                            deck_container.cards.forEach(function (card){
                                if(card.$el.className === "card")  {
                                    end = 0;
                                    return true;
                                }
                                if(card.$el.style["z-index"] >= 200){
                                    if(record_suit==null) record_suit = card;
                                    else if(card.i !== record_suit.i && card.suit === record_suit.suit){
                                        if(GAME === 0) player1 = player_one_init("player1");
                                        else player2 = player_one_init("player2");
                                        record_suit = null;
                                    }
                                    else record_suit = card;
                                    card.$el.style["z-index"] = record;
                                    record++;
                                    c_click = 0;
                                    if (GAME === 0 ) {
                                        GAME = 1;
                                        action_add("div.bgImg2.footer.player2");
                                        action_remove("div.bgImg1.header.player1");
                                    }
                                    else {
                                        GAME = 0;
                                        action_remove("div.bgImg2.footer.player2");
                                        action_add("div.bgImg1.header.player1");
                                    }
                                    return false;
                                }
                            });

                            if(end === 1) {
                                $(".end").css("display", "");
                                let p1 = 0;
                                player1.cards.forEach(function (card){
                                    if(card.$root != null) p1++;
                                });
                                let p2 = 0;
                                player2.cards.forEach(function (card){
                                    if(card.$root != null) p2++;
                                });
                                $("p.text1").text(p1);
                                $("p.text2").text(p2);
                                function index() {
                                    window.location.href = "index.html";
                                }
                                function s1() {
                                    $(".success1").css("display", "");
                                    $(".photo").css("display", "none");
                                }
                                function s2() {
                                    $(".success2").css("display", "");
                                    $(".photo").css("display", "none");
                                }
                                if(p1>p2) setInterval(s2, 2000);
                                else if(p1<p2) setInterval(s1, 2000);
                                setInterval(index, 5000);
                                return false;
                            }
                            chick_mp1 = 0;
                        }
                        setTimeout(f, 2000);
                        return false;
                    }
                });

                event.stopPropagation();
            }

            function p2_mouseenter(card){
                let vw = $(window).width();
                let origin = card.currentTarget.style.transform;
                card.currentTarget.style["z-index"] = parseInt(card.currentTarget.style["z-index"]) + 200;
                card.currentTarget.style.transform = origin + "perspective(" + vw * 0.8 + "px) translateZ(" + vw * 0.10 + "px)";
                event.stopPropagation();
            }

            function p2_mouseleave(card){
                let origin = card.currentTarget.style.transform.split(" ");
                origin = origin.slice(0, origin.length - 2).join(" ");
                card.currentTarget.style["z-index"] = parseInt(card.currentTarget.style["z-index"]) - 200;
                card.currentTarget.style.transform = origin;
                event.stopPropagation();
            }

            let chick_mp2 = 0;
            function p2_mousedown(){
                if(GAME === 0 || chick_mp2 === 1) return;
                chick_mp2 = 1;
                background_move();
                let t = $(this);
                player2.cards.forEach(function (card) {
                    if (card.$el.className === t.attr("class")) {
                        card.unmount();
                        let label = null;
                        deck_container.cards.forEach(function (c) {
                            if(c.i === card.i){
                                label = c;
                                return false
                            }
                        });
                        label.mount($("#container .deck")[0]);
                        label.$el.style["z-index"] = parseInt(label.$el.style["z-index"]) + 200;


                        function f() {
                            let end = 1;
                            deck_container.cards.forEach(function (card){
                                if(card.$el.className === "card")  {
                                    end = 0;
                                    return true;
                                }
                                if(card.$el.style["z-index"] >= 200){
                                    if(record_suit==null) record_suit = card;
                                    else if(card.i !== record_suit.i && card.suit === record_suit.suit){
                                        if(GAME === 0) player1 = player_one_init("player1");
                                        else player2 = player_one_init("player2");
                                        record_suit = null;
                                    }
                                    else record_suit = card;
                                    card.$el.style["z-index"] = record;
                                    record++;
                                    c_click = 0;
                                    if (GAME === 0 ) {
                                        GAME = 1;
                                        $("#player2 .card").on("mousedown", p2_mousedown);
                                        action_add("div.bgImg2.footer.player2");
                                        action_remove("div.bgImg1.header.player1");
                                    }
                                    else {
                                        GAME = 0;
                                        $("#player1 .card").on("mousedown", p1_mousedown);
                                        action_remove("div.bgImg2.footer.player2");
                                        action_add("div.bgImg1.header.player1");
                                    }
                                    return false;
                                }
                            });
                            if(end === 1) {
                                $(".end").css("display", "");
                                let p1 = 0;
                                player1.cards.forEach(function (card){
                                    if(card.$root != null) p1++;
                                });
                                let p2 = 0;
                                player2.cards.forEach(function (card){
                                    if(card.$root != null) p2++;
                                });
                                $("p.text1").text(p1);
                                $("p.text2").text(p2);
                                function index() {
                                    window.location.href = "index.html";
                                }
                                function s1() {
                                    $(".success1").css("display", "");
                                    $(".photo").css("display", "none");
                                }
                                function s2() {
                                    $(".success2").css("display", "");
                                    $(".photo").css("display", "none");
                                }
                                if(p1>p2) setInterval(s2, 2000);
                                else if(p1<p2) setInterval(s1, 2000);
                                setInterval(index, 5000);
                                return false;
                            }
                            chick_mp2 = 0;
                        }
                        setTimeout(f, 2000);
                        return false;
                    }
                });
                event.stopPropagation();
            }

            function player_one_init(player) {
                background_get_p();

                if ($("#"+player+" .deck")) {
                    $("#"+player+" .deck").remove();
                    $("#"+player).attr("style", "");
                }

                let $label = document.getElementById(player);
                let deck = Deck();
                deck.mount($label);
                let more = null;
                if(player === "player1" && player1) more = player1;
                else if(player === "player2" && player2) more = player2;

                deck_container.cards.forEach(function (label){
                    if(label.$el.className === "card"){
                        deck.cards[label.i].unmount();
                    }
                    else if(more && more.cards[label.i].$root ){
                        deck.cards[label.i].unmount();
                    }
                    else if(label.$root){
                        deck_container.cards[label.pos].unmount();
                    }
                });

                deck.intro();
                deck.bysuit();
                if(player === "player1"){
                    $("#player1 .card").on("mouseenter", p1_mouseenter);
                    $("#player1 .card").on("mouseleave", p1_mouseleave);
                    $("#player1 .card").on("mousedown", p1_mousedown);
                }
                else if(player === "player2"){
                    $("#player2 .card").on("mouseenter", p2_mouseenter);
                    $("#player2 .card").on("mouseleave", p2_mouseleave);
                    $("#player2 .card").on("mousedown", p2_mousedown);
                }
                setTimeout(start_init, 3000);

                function start_init() {
                    $("#"+player).css({
                        "animation-name": player + "_change_start",
                        "animation-duration":"2s",
                        "animation-fill-mode":"forwards"
                    })
                }

                return deck;
            }

            function init(label) {
                let $label = document.getElementById(label);
                let deck = Deck();
                deck.mount($label);
                return deck
            }
        });