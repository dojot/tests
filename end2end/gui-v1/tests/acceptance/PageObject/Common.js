let I = actor();

module.exports = {

    init(i) {
        I = i;
    },

    clickDiscard() {
        I.click('#auth-cancel');
    },

    clickSave() {
        I.click('#auth-save');
    },

    clickRemove() {
        I.click('#auth-delete');
    },

    clickCardByName(name) {
        I.waitForElement(locate('.card-size').find('div').withAttr({ title: name }));
        I.click(locate('.card-size').find('div').withAttr({ title: name }));
    },

    checkExistCard(name) {
        I.seeElement(locate('.card-size').find('div').withAttr({ title: name }));
    },

    checkNonExistCard(name) {
        I.dontSeeElement(locate('.card-size').find('div').withAttr({ title: name }));
    },


};
