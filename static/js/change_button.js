function change_buttons(first_connect)
    {        
        function visible_last_button(){
            if(schedule_data.length == (max_class-1)){
                button_list[(max_class-1)].style.display = "none";
            }
            else{
                button_list[(max_class-1)].style.display = "inline";
            }
        }
        
        function set_onclick(){
            for(var subject = 0; subject<schedule_data.length; subject++)
            {
                button_list[subject].innerText = schedule_data[subject];
                button_list[subject].onclick =  function(){
                        if(Object.keys(select_data).indexOf(schedule_data[this.id]) != -1){
                            var url = window.location.href+'/select/' + schedule_data[this.id]
                            location.href = url;
                        }

                        else{                        
                            var url = data['url'][schedule_data[this.id]];
                            count_zoom_open(schedule_data[this.id],url);
                            if(hyperlink === false)
                            {
                                var url  = "https://zoom.us/j/" +  url.split("no=")[1];

                            }
                            window.open(url, "_parent");
                        }
                        }

                }
        }
        
        if (first_connect){
            var today = new Date().getDay() - 1
            if(today == -1){
                today = 0
            }
            else if(today == 5){
                today = 4
            }
        }
        else {
            var today =  Number(document.querySelector("#id-week").value) - 1
            
        }
        document.querySelector("#id-week").options[today].selected = true; 
    
        schedule_data = data['schedule'][today];
        var button_list = document.querySelectorAll("button");

        visible_last_button()
        set_onclick()
        
    }
