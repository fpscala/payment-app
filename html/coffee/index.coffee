$ ->
  Api = ''
  window.addEventListener 'pywebviewready', ->
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
    directionsList: []
    totalPayment: 0
    list: [1..9]

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

  vm.currentDateTime(convertIntToDateTime(new Date()))
  setInterval ->
    vm.currentDateTime(convertIntToDateTime(new Date()))
  , 1000

  setTimeout ->
    getAllDirections()
  , 1000

  getAllGroups = (id) ->
    if id
      Api.get_groups().then (response) ->
        vm.groupsList(response.filter (e) -> e.direction_id == id)

  getAllTeachers = (teacherId) ->
    if teacherId
      Api.get_teachers().then (response) ->
        tIndex = indexOfByObject(response, 'id', teacherId)
        vm.payment.teacherName(response[tIndex]?.name)

  getLastPaymentId = ->
    Api.get_last_payment_id().then (response) ->
      vm.payment.id(response)

  getAllDirections = ->
    Api.get_directions().then (response) ->
      vm.directionsList(response)
      getLastPaymentId()

  vm.payment.directionId.subscribe (id) ->
    if id
      getAllGroups(id)

  vm.payment.groupId.subscribe (id) ->
    if id
      Api.get_students(id).then (response) ->
        vm.studentsList.removeAll()
        for student in response
          student.fullname = student.firstname + " " + student.lastname
          vm.studentsList.push(student)
        index = indexOfByObject(vm.groupsList(), 'id', id)
        teacherId = vm.groupsList()[index]?.teacher_id
        getAllTeachers(teacherId)

  vm.payment.studentId.subscribe (id) ->
    if id
      Api.get_payments(id).then (response) ->
        vm.paymentList(response)
        index = indexOfByObject(vm.studentsList(), 'id', id)
        vm.payment.studentFullName(vm.studentsList()[index]?.fullname)

  vm.getTotalPayment = (reports) ->
    sum = 0
    for report in reports
      sum += report.debt
    vm.totalPayment(vm.totalPayment() + sum)
    sum - reports[0].price_group

  vm.addPayment = ->
    toastr.clear()
    if !vm.payment.id()
      toastr.error("Iltimos chek raqamini kiriting!")
      return no
    else if !vm.payment.type()
      toastr.error("Iltimos to'lov turini kiriting!")
      return no
    else if !vm.payment.price()
      toastr.error("Iltimos summani kiriting!")
      return no
    else if !vm.payment.month()
      toastr.error("Iltimos qaysi oy uchun to'lamoqchiligingizni kiriting!")
      return no
    else if !vm.payment.groupId()
      toastr.error("Iltimos guruhni tanlang!")
      return no
    else
      data = ko.mapping.toJS(vm.payment)
      data.id = parseInt(data.id)
      Api.add_payment(data).then (response) ->
        ko.mapping.fromJS(defaultPayment, {}, vm.payment)
        vm.paymentList.removeAll()
        toastr.success(response)
        getLastPaymentId()

  vm.printPayment = ->
    toastr.clear()
    if !vm.payment.id()
      toastr.error("Iltimos chek raqamini kiriting!")
      return no
    else if !vm.payment.type()
      toastr.error("Iltimos to'lov turini kiriting!")
      return no
    else if !vm.payment.price()
      toastr.error("Iltimos summani kiriting!")
      return no
    else if !vm.payment.month()
      toastr.error("Iltimos qaysi oy uchun to'lamoqchiligingizni kiriting!")
      return no
    else if !vm.payment.groupId()
      toastr.error("Iltimos guruhni tanlang!")
      return no
    else
      data = ko.mapping.toJS(vm.payment)
      data.id = parseInt(data.id)
      Api.print_payment(data).then (response) ->
        ko.mapping.fromJS(defaultPayment, {}, vm.payment)
        vm.paymentList.removeAll()
        toastr.success(response)
        getLastPaymentId()

  ko.applyBindings {vm}