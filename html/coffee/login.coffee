$ ->
  Api = ''
  window.addEventListener 'pywebviewready', ->
    Api = pywebview.api

  vm = ko.mapping.fromJS
    login: ''
    password: ''

  vm.onSubmit = ->
    toastr.clear()
    if !vm.login()
      toastr.error("Iltimos guruh ochilgan vaqtni kiriting!")
      return no
    else if !vm.password()
      toastr.error("Iltimos guruh nomini kiriting!")
      return no
    else
      Api.check_user(vm.login(), vm.password()).then (response) ->
        Api.logger(response)
        if response.code is 401
          toastr.error(response.error)

  ko.applyBindings {vm}