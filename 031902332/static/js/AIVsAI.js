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

            function mouseup(){
                if(!c_click || $(this).attr("id") === "show") return;
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
                            card.$el.style["z-index"] = record;
                            record++;
                            return false;
                        }
                    });
                    if(end === 1) {
                        $(".end").css("display", "");
                        let p1 = 0;
                        player1.cards.forEach(function (card){
                            if(card.$root) p1++;
                        });
                        let p2 = 0;
                        player2.cards.forEach(function (card){
                            if(card.$root) p2++;
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
                    c_click = 0;
                    if (GAME === 0 ) {
                        GAME = 1;
                        action_add("div.bgImg2.footer.player2");
                        action_remove("div.bgImg1.header.player1");
                        AI_action();
                    }
                    else {
                        GAME = 0;
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

            let chick_mp1 = 0;
            function p1_mousedown(t){
                if(GAME !== 0 || chick_mp1 === 1) return;
                chick_mp1 = 1;

                $("#container .card").off("mouseenter");
                $("#container .card").off("mouseleave");
                $("#container .card").off("mouseup");

                background_move();
                player1.cards.forEach(function (card) {
                    if (card.$el.className === t.className) {
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
                                        AI_action(GAME);
                                    }
                                    else {
                                        GAME = 0;
                                        action_remove("div.bgImg2.footer.player2");
                                        action_add("div.bgImg1.header.player1");
                                        AI_action(GAME);
                                    }
                                    return false;
                                }
                            });
                            if(end === 1) {
                                $(".end").css("display", "");
                                let p1 = 0;
                                player1.cards.forEach(function (card){
                                    if(card.$root) p1++;
                                });
                                let p2 = 0;
                                player2.cards.forEach(function (card){
                                    if(card.$root) p2++;
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
                            $("#container .card").on("mouseenter", c_seen);
                            $("#container .card").on("mouseleave", c_leave);
                            $("#container .card").on("mouseup", mouseup);
                        }
                        setTimeout(f, 2000);
                        return false;
                    }
                });
            }

            let chick_mp2 = 0;
            function p2_mousedown(t){
                if(GAME !== 1 || chick_mp2 === 1) return;
                chick_mp2 = 1;

                $("#container .card").off("mouseenter");
                $("#container .card").off("mouseleave");
                $("#container .card").off("mouseup");

                background_move();
                player2.cards.forEach(function (card) {
                    if (card.$el.className === t.className) {
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
                                        AI_action(GAME);
                                    }
                                    else {
                                        GAME = 0;
                                        action_remove("div.bgImg2.footer.player2");
                                        action_add("div.bgImg1.header.player1");
                                        AI_action(GAME);
                                    }
                                    return false;
                                }
                            });
                            if(end === 1) {
                                $(".end").css("display", "");
                                let p1 = 0;
                                player1.cards.forEach(function (card){
                                    if(card.$root) p1++;
                                });
                                let p2 = 0;
                                player2.cards.forEach(function (card){
                                    if(card.$root) p2++;
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
                            $("#container .card").on("mouseenter", c_seen);
                            $("#container .card").on("mouseleave", c_leave);
                            $("#container .card").on("mouseup", mouseup);
                        }
                        setTimeout(f, 2000);
                        return false;
                    }
                });
            }

            function AI_action(play) {
                let data_dict = {
                    "pokers_total":0, "pokers_0":0, "pokers_1":0, "pokers_2":0, "pokers_3":0,
                    "used_total":0, "used_0":0, "used_1":0, "used_2":0, "used_3":0, "used_head":0,
                    "player_one_total":0, "player_one_0":0, "player_one_1":0, "player_one_2":0, "player_one_3":0,
                    "player_two_total":0, "player_two_0":0, "player_two_1":0, "player_two_2":0, "player_two_3":0
                };

                deck_container.cards.forEach(function (card) {
                    if(card.$el.style["z-index"] >= 200) {
                        data_dict["used_head"] = card.suit;
                    }
                    if(card.$root && card.$el.className === "card"){
                        data_dict["pokers_total"] += 1;
                        data_dict["pokers_" + card.suit] += 1;
                    }
                    else if(card.$root && card.$el.id === "show"){
                        data_dict["used_total"] += 1;
                        data_dict["used_" + card.suit] += 1;
                    }
                });

                if(player1){
                    player1.cards.forEach(function (card) {
                        if(card.$root){
                            data_dict["player_one_total"] += 1;
                            data_dict["player_one_" + card.suit] += 1;
                        }
                    });
                }

                if(player2){
                    player2.cards.forEach(function (card) {
                        if(card.$root){
                            data_dict["player_two_total"] += 1;
                            data_dict["player_two_" + card.suit] += 1;
                        }
                    });
                }


                $.ajax({
                  type: 'POST',
                  url: "http://127.0.0.1:5000/play",
                  contentType: "application/json",
                  data: JSON.stringify(data_dict),
                  success: success,
                  dataType: "json"
                });

                function success(data, textStatus, jqXHR) {
                    let action = data["action"];
                    console.log(action);
                    let player = null, player_total = null, player_action = null;
                    let p_mousedown = null;
                    if(play === 0){
                        player = player1;
                        player_total = "player_one_total";
                        player_action = "player_one_";
                        p_mousedown = p1_mousedown;
                    }
                    else{
                        player = player2;
                        player_total = "player_two_total";
                        player_action = "player_two_";
                        p_mousedown = p2_mousedown;
                    }
                    if(action === 0 || player == null || data_dict[player_total] === 0) {
                        let array = new Array();
                        deck_container.cards.forEach(function (card) {
                            if(card.$root && card.$el.className === "card"){
                                array.push(card.pos);
                            }
                        });
                        let index = Math.floor(Math.random() * array.length);
                        let z = deck_container.cards[array[index]].$el;

                        let vw = $(window).width();
                        let origin = z.style["transform"];
                        z.style["z-index"] = parseInt(z.style["z-index"]) + 200;
                        z.style["transform"] = origin + "perspective(" + vw * 0.8 + "px) translateZ(" + vw * 0.10 + "px)";
                        AI_mouseup(z);
                    }
                    else{
                        if(data_dict[player_action + (action - 1)] === 0){
                            let array = new Array();
                            player.cards.forEach(function (card) {
                                if(card.$root && card.$el.className !== "card"){
                                    array.push(card.pos);
                                }
                            });
                            let index = Math.floor(Math.random() * array.length);
                            let z = player.cards[array[index]].$el;
                            p_mousedown(z);
                            return false;
                        }
                        player.cards.forEach(function (card) {
                            if(card.$root && card.$el.className !== "card" && card.suit === (action - 1)){
                                p_mousedown(card.$el);
                                return false;
                            }
                        });

                    }
                }
            }

            function AI_mouseup(t){
                background_move();
                $("#container .card").off("mouseenter");
                $("#container .card").off("mouseleave");
                $("#container .card").off("mouseup");
                deck_container.cards.forEach(function (card){
                    if(card.$el.style["z-index"] === t.style["z-index"]){
                        card.setSide('front');
                    }
                });

                t.id = "show";
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
                            return false;
                        }
                    });
                    if(end === 1) {
                        $(".end").css("display", "");
                        let p1 = 0;
                        player1.cards.forEach(function (card){
                            if(card.$root) p1++;
                        });
                        let p2 = 0;
                        player2.cards.forEach(function (card){
                            if(card.$root) p2++;
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

                    c_click = 0;
                    if (GAME === 0 ) {
                        GAME = 1;
                        action_add("div.bgImg2.footer.player2");
                        action_remove("div.bgImg1.header.player1");
                        AI_action(GAME);
                    }
                    else {
                        GAME = 0;
                        action_remove("div.bgImg2.footer.player2");
                        action_add("div.bgImg1.header.player1");
                        AI_action(GAME);
                    }

                    $("#container .card").on("mouseenter", c_seen);
                    $("#container .card").on("mouseleave", c_leave);
                    $("#container .card").on("mouseup", mouseup);
                }
                setTimeout(f, 2000);
            }

            function player_one_init(player) {
                background_get_p();

                if ($("#"+player+" .deck")!=null) {
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
                    else if(more!=null && more.cards[label.i].$root !=null){
                        deck.cards[label.i].unmount();
                    }
                    else if(label.$root){
                        console.log("33333");
                        console.log(label);
                        deck_container.cards[label.pos].unmount();
                    }
                });

                deck.intro();
                deck.bysuit();
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