'use strict'

$('#sideBar').sidebar('hide')
$('#language').dropdown({
  ignoreDiacritics: true,
  sortSelect: true,
  fullTextSearch: 'exact'
})

// $('#SignIn_Button')(window.open('../templates/login.html'))

$('#privilege').dropdown({
  ignoreDiacritics: true,
  sortSelect: true,
  fullTextSearch: 'exact'
})
