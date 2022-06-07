$(document).ready(function(){
 $.getJSON("/fetchallstates",{ajax:true},function(data){
 $.each(data,function(index,item){
   $('#state').append($('<option>').text(item[1]).val(item[0]))
 })
 })
 $('#state').change(function(){
  $.getJSON("/fetchallcities",{ajax:true,stateid:$('#state').val()},function(data){
    $('#city').empty()
     $('#city').append($('<option>').text('-city-'))
    $.each(data,function(index,item){
      $('#city').append($('<option>').text(item[2]).val(item[1]))

    })
  })
})
$('#picture').change(function(){
  var file=picture.files[0]
  pic.src=URL.createObjectURL(file)
})
})

