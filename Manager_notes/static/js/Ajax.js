$(document).ready(function(){
    id = 0;
    if($.cookie('sort') != null && $("#all_notes").children().length != 0){
        var s_category = $.evalJSON($.cookie('sort')).s_category;
        var s_cret = $.evalJSON($.cookie('sort')).s_cret;
        $("#sort_category").val(s_category);
        $("#sort_cret").val(s_cret);
        var c=[];
        var r = document.getElementById("all_notes");
        for(var i = 0; i < $.evalJSON($.cookie('sort')).s_data.length; i++) {
            c[i] = document.getElementById($.evalJSON($.cookie('sort')).s_data[i])
        }
        for (var i = 0; i < c.length; i++){
            r.appendChild(c[i]);
        }
    } // Сортировка данных относительно куки файлов

    $(function now(){
        if($.cookie('now') == null){
            if($.cookie('sort') != null){
                var r = $.cookie('sort');
                $.cookie('sort', r, {
                    expires: 360
                });
                $.cookie('now', true, {
                    expires: 180
                })
            }
        }
        else{
            if($.cookie('sort') == null){
            $.cookie('now', null, {
                expires: -1
            })
        }
       }
    }); // Провкрка куки файлов и обновление их данных если существуют

    $('.notes').on('click', '#del', function(){
        id = $(this).parent().attr("id");
        $.ajax({
                url: "del_"+id+"/",
                type: "POST",
                data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value') },
                success: function (data) {
                    if(data == 1){
                        var r = $('#'+id);
                        r.remove();
                        id = 0;
                        $("#sort").click()
                    }
                    else{
                        window.location.href = "/";
                    }
                    $('#sort').trigger('click');
                }
        });
    }); // Удаление заметки

    $('.notes').on('click', '#red', function(){
        id = $(this).parent().attr("id");
        var parent = $(this).parent();
        var text = parent.children('#header_text').children('#text').html();
        tinymce.get('id_note_text').setContent(text);
        var header = parent.children('#header_text').children('#header').text();
        $('#new_header').val(header);
        var favorites = parent.children('#category_time_favorites').children('#favorites').text();
        if(favorites == "Избранное"){
            $('#new_favorites').prop("checked", true)
        }
        var category = parent.children('#category_time_favorites').children('#category').text();
        $('#new_category option').each(function(){
            if(this.text == category){
                this.selected = true;
            }
        });
        $('html, body').animate({scrollTop: 0}, 0);
    }); // Редактирование заметки

    var exit = $('#exit_note');
    exit.click(function(){
        tinymce.get('id_note_text').setContent("");
        $('#new_header').val("");
        $('#new_favorites').attr("checked", false);
        $("#new_category").val(1);
        id = 0;
    }); //Очистка полейя для редактирования и добавления заметки

    var dob = $('#new');
    dob.click(function(){
        var text = tinymce.get('id_note_text').getContent();
        var header = $('#new_header').val();
        var favorites = $('#new_favorites').prop("checked");
        var category = $('#new_category').val();
        if(text != "" && header!= ""){
            $.ajax({
                url: "new_"+id+"/",
                type: "POST",
                data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value'),
                        text:text, header:header, favorites:favorites, category:category
                },
                success: function (jsondata) {
                    if(jsondata == 'error') location.href = '/';
                    if(jsondata == 1 | jsondata.data == 0) {
                        var parent = $('#'+id);
                        if(jsondata == 1){
                            var ctf = parent.children('#category_time_favorites');
                            ctf.children('#category').text($("#new_category option:selected").text());
                            if(favorites){
                                ctf.children('#favorites').text("Избранное").css('color', 'green')
                            }
                            else{
                                ctf.children('#favorites').text("Не избранное").css('color', 'red')
                            }
                            var ht = parent.children('#header_text');
                            ht.children('#header').text(header);
                            ht.children('#text').html(text);
                        }
                        else{
                            var all_notes = $('#all_notes');
                            var n_category = $("#new_category option:selected").text();
                            if(favorites){
                                var n_favorites = "Избранное";
                                var color = "green";
                            }
                            else{
                                var n_favorites = "Не избранное";
                                var color = "red";
                            }
                            var html = "<div style='border: 2px; border-color: #404040;'id="+jsondata.pk+">"+
                            "<p id='category_time_favorites' style='margin-right: 20px; font-size: 12px;'>"+
                            "<output id='category' style='margin-left: 30px; font-size: 20px; border: 2px solid'>"+
                            n_category+"</output> <b style='border: 2px solid'>"+jsondata.tim+" </b> <output id='favorites'"+
                            "style=' color: "+color+"; font-size: 15px; margin-left: 3%;'>"+n_favorites+"</output></p>"+
                            "<div id='header_text' style='border: 2px solid; width: 99.6%;'>"+
                            "<h5 id='header' style='word-wrap: break-word; margin-left: 100px; width: 80%'>"+header+"</h5>"+
                            "<div id='text' style='word-wrap: break-word; width: 96%; margin-left: 15px;' >"+text+"</div></div>" +
                            "<div id='href_div' style='float: right; margin-top: 10px'>" +
                            "<button class='button' id='open_href'>Открыть прямую ссылку</button></div>"+
                            "<button class='button' id='red' style='margin-top: 10px' >Редактировать</button> "+
                            "<button class='button' id='del' style='margin-top: 10px'>Удалить</button<hr></div>";
                            all_notes.prepend(html);
                        }
                        tinymce.get('id_note_text').setContent("");
                        $('#new_header').val("");
                        $('#new_favorites').attr("checked", false);
                        $("#new_category").val(1);
                        id = 0;
                        $('#sort').trigger('click');
                    }
                    else{
                        window.location.href = "/";
                    }
                }
            });
        }
    }); // Добавление новой или отредактированой заметки

    $('#div_new_category').on('click', '#new_plus', function(){
        $('#new_plus').remove();
        $('#div_new_category').html("<output style='color: green; font-size: 20px'>|</output> "+
        "<input type='text' id='text_category' class='tiny_stile' widtn='100px'></input> "+
        "<button id='plus_category' class='button'>Добавть</button> "+
        "<button id='del_category' class='button'>Удалить</button> "+
        "<button id='exit_category' class='button'>Отменить</button> "+
        "<output style='color: green; font-size: 20px'>|</output>");
     }); // Отображение полей дляредактирования категорий

    $('#div_new_category').on('click', '#plus_category', function(){
        var text = $("#text_category").val();
        if(text != ""){
            $.ajax({
                url: "category_plus/",
                type: "POST",
                data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value'), category:text },
                success: function (jsondata) {
                    if(jsondata == 'error') location.href = '/';
                    if (jsondata.stat == 0){
                        $("#text_category").val("Уже существует");
                    }
                    else{
                        if(jsondata.stat == 1){
                            $("#text_category").val("");
                            var child = $("#new_category").children();
                            if (child.length == 1){
                                $("#new_category").append( $('<optgroup label="Свои"></outgroup>'));
                            }
                            $("#new_category").children("optgroup[label=Свои]").append( $('<option value="'+jsondata.id+'">'+text+'</option>'));
                        }
                        else{
                            $("#text_category").val("Ошибка");
                        }
                    }

                }
            });
        }
    }); // Добавлнение новой категории

    $('#div_new_category').on('click', '#del_category', function(){
        var text = $("#text_category").val();
        if(text != ""){
            $.ajax({
                url: "category_del/",
                type: "POST",
                data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value'), category:text },
                success: function (jsondata) {
                    if(jsondata == 'error') location.href = '/';
                    if (jsondata.stat == 0){
                        $("#text_category").val("Не существует");
                    }
                    else{
                        if(jsondata.stat == 1){
                            $("#text_category").val("");
                            var opt = $("#new_category").children("optgroup[label=Свои]").children( $('<option value="'+jsondata.id+'">'+text+'</option>'));
                            opt.remove();
                            var opt = $("#new_category").children("optgroup[label=Свои]");
                            if(opt.length == 1 ){
                                opt.remove();
                            }
                            parent = [];
                            $("#all_notes").children().each(function(){
                               if($(this).children().children("#category").text() == text){
                                   $(this).remove()
                               }
                            });
                            $('#sort').trigger('click');

                        }
                        else{
                            $("#text_category").val("Ошибка");
                        }
                    }

                }
            });
        }
    }); // Удаление категории

    $('#div_new_category').on('click', '#exit_category', function(){
        $('#div_new_category').html("<output style='color: green; font-size: 20px'>|</output>"+
                                    "<button id='new_plus' class='button'>Редактор категорий</button>"+
                                    "<output style='color: green; font-size: 20px'>|</output><br>") }); // Отмена работы для редактора категорий

    var sort = $("#sort");
    sort.click(function(){
        var s_category = $("#sort_category").val();
        var s_cret = $("#sort_cret").val();
        $.ajax({
            url: "sorted/",
            method: "POST",
            data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value'), s_category:s_category, s_cret:s_cret},
            success: function(data){
                if(data == 'error') location.href = '/';
                var sort = {s_category:s_category, s_cret:s_cret, s_data:data};
                $.cookie('sort', $.toJSON(sort));
                var c=[];
                var r = document.getElementById("all_notes");
                for(var i = 0; i < data.length; i++) {
                    c[i] = document.getElementById(data[i])
                }
                for (var i = 0; i < c.length; i++){
                    r.appendChild(c[i]);
                }
            }
        });

    }); // Сортировка категорий

    $('#search_div').on('click', '#search_button_cretery', function(){
        if($("#all_notes").children().length != 0) {
            var cretery = $("#search_category").val()
            if (cretery == 1) {
                html = "<output style='color: green; font-size: 25px'>|</output> " +
                "<input type='text' id='datepicker' value='Нажми' style='width: 100px'> " +
                "<button class='button' id='search' name='1'>Поиск</button> " +
                "<button class='button' id='exit_search'>Отмена</button> " +
                "<output style='color: green; font-size: 25px'>|</output>"
            }
            if (cretery == 2) {
                html = "<output style='color: green; font-size: 25px'>|</output> " +
                "<input type='text' id='search_data'> " +
                "<button class='button' id='search' name='2'>Поиск</button> " +
                "<button class='button' id='exit_search'>Отмена</button> " +
                "<output style='color: green; font-size: 25px'>|</output>"
            }
            if (cretery == 3) {
                html = "<output style='color: green; font-size: 25px'>|</output> " +
                "<select id='search_data' size='1' class='tiny_stile' style='width: 175px;'> " +
                $("#new_category").html() +
                "</select> <button class='button' id='search' name='3'>Поиск</button> " +
                "<button class='button' id='exit_search'>Отмена</button> " +
                "<output style='color: green; font-size: 25px'>|</output>"
            }
            if (cretery == 4) {
                html = "<output style='color: green; font-size: 25px'>|</output> " +
                "<label>Избранное :</label><input id='serch_data' type='checkbox'> " +
                "<button class='button' id='search' name='4'>Поиск</button> " +
                "<button class='button' id='exit_search'>Отмена</button> " +
                "<output style='color: green; font-size: 25px'>|</output>"
            }
            $('#search_div').html(html);
        }
    }); // Показать поля для для фильтрации относительно выбора пользователя

    $('#search_div').on('click', '#search', function(){
        var idi = $(this).attr('name');
        if(idi == 1){
            var data = $("#datepicker").val()
        }
        if(idi == 2 || idi == 3){
            var data = $("#search_data").val()
        }
        if(idi == 4) {
            var data = $("#serch_data").prop("checked");
            data = data ? 1 : 2
        }
        if(data != "Нажми" && data != ""){
            $.ajax({
                url: "search/",
                type: "POST",
                data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value'), idi:idi, data:data },
                success: function (data) {
                    if(data == 'error') location.href = '/';
                    if(data == 'not') alert("Данные не найдены");
                    else {
                        var e = $('div#all_notes > div');
                        for (var i = 0; i < e.length; i++) {
                            var t = $(e[i]).attr('id');
                            var y = -1;
                            if(data.length==1){
                                if(t == data[0]){
                                    y = 0;
                                }
                            }else{
                                $.each(data, function(){
                                    if(this == t){
                                        y = 1
                                    }
                                });
                            }
                            if(y == -1) {
                                $(e[i]).css('display', 'none')
                            }
                            else {
                                $(e[i]).css('display', 'block');
                            }

                        }
                    }
                }
        });
        }

    }); // поиск нужных заметок
    $('#search_div').on('click', '#exit_search', function(){
        html = "<output style='color: green; font-size: 25px'>|</output> " +
                "<select id='search_category' size='1' class='tiny_stile'> "+
                "<option value='1'>Дата</option>"+
                "<option value='2'>Заголовок</option>"+
                "<option value='3'>Категория</option>"+
                "<option value='4'>Избранное</option></select> "+
                "<button id='search_button_cretery' class='button'>Выбрать критерий для поиска</button> "+
                "<output style='color: green; font-size: 25px'>|</output>";
        $('#search_div').html(html);
        var e = $('div#all_notes > div');
        for (var i = 0; i < e.length; i++) {
            var t = $(e[i]).attr('id');
            $(e[i]).css('display', 'block');
            }
        }); // Отмена поиска заметок

    $('#search_div').on('focus', '#datepicker', function(){
        $("#datepicker").datepicker();
        $("#datepicker").datepicker($.datepicker.regional["ru"]);
    }); //Отображение календаря


    $('.notes').children().on('click', '#open_href', function() {
        var id = $(this).parent().parent().attr("id");
        $.ajax({
            url: "href_open_" + id + "/",
            type: "POST",
            data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value')},
            success: function (data) {
                if (data == 'error') location.href = '/';
                var dat = "http://127.0.0.1:8100" + data;
                html = "<a id='href_uuid' style='font-size: 10px;' href='"+dat+"'></a> "+
                "<button class='button' id='close_href'>Закрыть прямую ссылку</button> ";
                $("#"+ id).children("#href_div").html(html);
                $("#"+ id).children("#href_div").children("#href_uuid").text(dat)
            }

        });
    }); // Открыть доступ по ссылке
    $('.notes').children().on('click', '#close_href', function() {
        var id = $(this).parent().parent().attr("id");
        $.ajax({
            url: "href_close_" + id + "/",
            type: "POST",
            data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value')},
            success: function (data) {
                if(data == 'error') location.href = '/';
                html = "<button class='button' id='open_href'>Открыть прямую ссылку</button>";
                $("#"+id).children("#href_div").html(html)
            }
        });
    }); // Закрыть доступ по ссылке
});
