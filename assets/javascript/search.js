$(document).ready(function(){
   $('#pattern').keyup(function(){

     $.getJSON('/finalproductalljson/',{pattern:$('#pattern').val()},function(data){

       var htm="<table class='table'><tr><th>ID</th><th>Final Product Name</th><th>Stock</th><th>Price</th></tr>"

        $.each(data,function(index,item){
            htm+="<tr> <th scope='rows'>"+item.finalproductid+"</th><td>"+item.finalproductname+"</td><td>"+item.stock+"</td><td>"+item.price+"</td></tr>"
            })

            htm+="</table>"
            $('#result').html(htm)


     })

   })

})