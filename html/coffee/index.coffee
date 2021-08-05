$ ->
  Api = pywebview.api
  
  defaultPayment =
    id: 0
    price: ''
    comments: ''
    type: ''
    month: ''
    groupId: ''
    studentId: ''
    teacherId: ''
    directionId: ''
    groupName: ''
    teacherName: ''
    studentFullName: ''

  vm = ko.mapping.fromJS
    currentDateTime: ''
    payment: defaultPayment
    groupsList: []
    paymentList: []
    studentsList: []
    teachersList: []
    allGroupsList: []
    directionsList: []
    totalPayment: 0
    list: [1..9]
    login: ''
    password: ''


  convertIntToDateTime = (intDate) ->
    if intDate
      moment(intDate).format('DD.MM.YYYY HH:mm')

  indexOfByObject = (array, attr, value) ->
    i = 0
    while i < array.length
      if array[i][attr] == value
        return i
      i += 1
    -1

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

  vm.currentDateTime(convertIntToDateTime(new Date()))
  setInterval ->
    vm.currentDateTime(convertIntToDateTime(new Date()))
  , 1000

  setTimeout ->
    getAllDirections()
  , 1000

  getAllGroups = ->
    Api.get_groups().then (response) ->
      Api.logger(response)
      vm.allGroupsList(response)

  getAllTeachers = ->
    Api.get_teachers().then (response) ->
      Api.logger(response)
      vm.teachersList(response)

  getLastPaymentId = ->
    Api.get_last_payment_id().then (response) ->
      Api.logger(response)
      vm.payment.id(response)

  getAllDirections = ->
    Api.get_directions().then (response) ->
      Api.logger(response)
      vm.directionsList(response)
      getAllGroups().then ->
        getLastPaymentId().then ->
          getAllTeachers()

  vm.payment.directionId.subscribe (id) ->
    vm.groupsList(vm.allGroupsList().filter (e) -> e.direction_id == id)

  vm.payment.groupId.subscribe (id) ->
    if id
      Api.get_students(id).then (response) ->
        Api.logger(response)
        for student in response
          student.fullname = student.firstname + " " + student.lastname
          vm.studentsList.push(student)
        index = indexOfByObject(vm.groupsList(), 'id', id)
        teacherId = vm.groupsList()[index]?.teacher_id
        tIndex = indexOfByObject(vm.teachersList(), 'id', teacherId)
        vm.payment.teacherName(vm.teachersList()[tIndex]?.name)

  vm.payment.studentId.subscribe (id) ->
    if id
      Api.get_students(id).then (response) ->
        Api.logger(response)
        vm.paymentList(response)
        index = indexOfByObject(vm.studentsList(), 'id', id)
        vm.payment.studentFullName(vm.studentsList()[index]?.fullname)

  ko.applyBindings {vm}