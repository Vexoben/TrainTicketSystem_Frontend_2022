'use strict'
$('#sideBar').sidebar('hide')
$('#language').dropdown({
  ignoreDiacritics: true,
  sortSelect: true,
  fullTextSearch: 'exact'
})

$('#privilege').dropdown({
  ignoreDiacritics: true,
  sortSelect: true,
  fullTextSearch: 'exact'
})

$('#rangestart').calendar({
  type: 'date',
  endCalendar: $('#rangeend')
})
$('#rangeend').calendar({
  type: 'date',
  startCalendar: $('#rangestart')
})
$('#start_time').calendar({
  type: 'time'
  // startCalendar: $('#rangestart')
})

$(document).ready(function () {
  $('#btAdd').click(function () {
    var rank = $('#stations').children().length - 1

    // $('#stations > template> input').attr('name',rank);

    var clone = $($('#stations > template').html())

    clone.attr('id', 'st' + rank)
    clone.find('input:eq(0)').attr('name', 'station_name_' + rank)
    clone.find('input:eq(1)').attr('name', 'travel_time_' + rank)
    clone.find('input:eq(2)').attr('name', 'stop_over_time_' + rank)
    clone.find('input:eq(3)').attr('name', 'price_' + rank)
    // clone.find('input:first').attr('name',"station_name_"+rank)
    // clone.find('input:first').attr('name',"station_name_"+rank)
    $('#stations > div:last').before(clone)
    //  var $st = $("#st1").clone();
    //   $("#stations").append(" <b>插入文本</b>.");
  })
})
