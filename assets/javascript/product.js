$(document).ready(function(){
   $.getJSON("/getcategoryjson",{ajax:true},function(data){
   $.each(data,function(index,item){
     $('#categoryid').append($('<option>').text(item[1]).val(item[0]))
  })

   })
 $('#categoryid').change(function(){
  $.getJSON("/getsubcategoryjson",{ajax:true,categoryid:$('#categoryid').val()},function(data){
    $('#subcategoryid').empty()
    $('#subcategoryid').append($('<option>').text('-Select Subcategory-'))
    $.each(data,function(index,item){
      $('#subcategoryid').append($('<option>').text(item[2]).val(item[1]))

    })
  })
})
$('#subcategoryid').change(function(){
  $('#productid').empty()
  $.getJSON("/getproductjson",{ajax:true,subcategoryid:$('#subcategoryid').val()},function(data){

    $('#productid').append($('<option>').text('-Select Product-'))
    $.each(data,function(index,item){
      $('#productid').append($('<option>').text(item[3]).val(item[2]))
})
})
})
      $(".pay").click(function(){
         var amt=$(this).attr('amount')
           alert(amt)
      })

})
