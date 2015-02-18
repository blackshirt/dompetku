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
    self.info = ko.observable('');
    self.amount = ko.observable('');
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