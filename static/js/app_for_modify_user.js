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
