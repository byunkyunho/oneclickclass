function direct_open(){
    var now = new Date(); ;
    var minutes = now.getMinutes() + now.getHours()*60;
    var open_class = false;
    for(var index=0;index< schedule_data.length ;index++)
    {

        if(minutes >=  Number(class_time[index].split(",")[0]) && minutes <=  Number(class_time[index].split(",")[1])){
            if(Object.keys(select_data).indexOf(schedule_data[index]) != -1){
                var url = window.location.href+'/select/' + schedule_data[index]
                location.href = url;
            }
        
            else{                        
                var url = data['url'][schedule_data[index]];
                count_zoom_open(schedule_data[index],url);

                if(hyperlink === false)
                {
                    var url  = "https://zoom.us/j/" +  url.split("no=")[1];
        
                }
                window.open(url, "_parent");
            }
            var open_class = true;
            break;     
        }
    }
    if(!open_class){
        alert('지금은 수업시간이 아닙니다.')
    }


}
