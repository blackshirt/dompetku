var TransaksiNamespace = {};

TransaksiNamespace.initTransactionEntryViewModel = function(transaction){
    var transactionViewModel = ko.validatedObservable({
        tid: ko.observable(transaction.tid),
        user: ko.observable(transaction.user),
        info: ko.observable(transaction.info).extend({ required: true }),
        amount: ko.observable(transaction.amount).extend({ required: true }).extend({ number: true }),
        transdate: ko.observable(transaction.transdate),
        memo: ko.observable(transaction.memo).extend({ required: true }),

    });

    var validationOptions =
      { insertMessages: true, decorateElement: true, errorElementClass: 'help-inline' };
    ko.validation.init(validationOptions);

    return transactionViewModel;
}

TransaksiNamespace.bindData = function(transaction) {


    // Create the view model
    TransaksiNamespace.viewModel =
      TransaksiNamespace.initTransactionEntryViewModel(transaction);
    ko.applyBindings(this.viewModel);
}

TransaksiNamespace.getTransactionEntries = function(user) {
    $.ajax({
        url: "/services/trans",
        type: 'post',
        data: "{'user':'1' }",
        contentType: 'application/json',
        cache: false,
        success: function (result) {
            TransaksiNamespace.bindData(result);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            var errorMessage = '';
            $('#message').html(jqXHR.responseText);
        }
    });
}


function transaksiEntri(data) {
    var self = this;
    self.tid = data.tid;
    self.user = data.user;
    self.info = data.info;
    self.amount = data.amount;
    self.transdate = data.transdate;
    self.memo = data.memo;
    
};

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
    success: function(response) {
    callback(eval("(" + response + ")"));
    }});
};

function transaksiViewModel() {
    var self = this;
    self.tid = ko.observable('');
    self.user = ko.observable('');
    self.transdate = ko.observable('');
    self.info = ko.observable('').extend({required: true});
    self.amount = ko.observable('').extend({
                required: true,
                number: true
                });
    self.memo = ko.observable('');
    

    self.addText = ko.observable('Add');
    self.resetText = ko.observable('Reset');
    self.selectedIndex = -1;

    self.transaksiEntries = ko.observableArray([]);
    
    self.total = ko.computed(function() {
        var tot = 0;
        for (var i = 0; i < self.transaksiEntries().length; i++)  {
               tot += self.transaksiEntries()[i]["amount"]
        }
        return tot;
    });

    self.add = function () {
        var entry = new transaksiEntri({
            info : self.info(),
            amount : self.amount(),
            memo : self.memo(),
            
        });

        self.transaksiEntries.push(entry);
    };

    self.addTransaksitoServer = function(){

            $.ajax({
                url: "/services/trans",
                type: "post",
                data: ko.toJSON({
                    info : self.info(),
                    amount : self.amount(),
                    memo : self.memo()
                }),
                contentType: "application/json",
                success: function(response){
                    console.log(response);
                    data = $.parseJSON(response)
                    self.transaksiEntries.push(new transaksiEntri(data));

                },
             error:function(jqXHR, textStatus, errorThrown) {
                console.log(errorThrown);
             }
        })
     };

    self.postTransaksi = function() {
        console.log('process form post to server');


        console.log('formValidation validate ');


        var self = this;
        console.log(ko.toJSON(self))
        $.ajax({
            url: '/services/trans',
            type: 'post',
            data: ko.toJSON(self),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function (jsondata) {
                self.transaksiEntries.push(new transaksiEntri(jsondata));

            }
        })
    };

    self.edit = function (transaksiEntri) {
        self.info(transaksiEntri.info);
        self.amount(transaksiEntri.amount);
        self.memo(transaksiEntri.memo);
    };

    self.delete = function (transaksiEntri) {
        self.transaksiEntries.destroy(transaksiEntri);
    };

    self.reset = function () {
    };

    self.load = function () {
        $.getJSON("/services/trans", function(allData) {
            var mappedEntri = $.map(allData, function(entry) { return new transaksiEntri(entry) });
        self.transaksiEntries(mappedEntri);
    });
    };

    self.post = function (transaksiEntri) {

    };

    self.load();
}
ko.applyBindings(new transaksiViewModel());