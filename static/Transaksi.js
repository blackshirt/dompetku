function transaksiEntri(data) {
    var self = this;
    self.info = data.info;
    self.amount = data.amount;
    self.memo = data.memo;
};


function transaksiViewModel() {
    var self = this;
    self.info = ko.observable('');
    self.amount = ko.observable(0);
    self.memo = ko.observable('');

    self.addText = ko.observable('Add');
    self.resetText = ko.observable('Reset');
    self.selectedIndex = -1;

    self.transaksiEntries = ko.observableArray([]);

    self.add = function () {
        var entry = new transaksiEntri({
            info : self.info(),
            amount : self.amount(),
            memo : self.memo()
        });

        self.transaksiEntries.push(entry);
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