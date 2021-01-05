let I = actor();

module.exports = {


    init(i) {
        I = i;
    },

    fillEmailAndSave(email) {
        I.fillField('email', email);
        I.fillField('confirmEmail', email);
        this.clickSave();
    },

    fillAndSave(user) {
        I.fillField('username', user.username);
        I.fillField('name', user.name);
        I.fillField('email', user.email);
        I.fillField('confirmEmail', user.email);
        I.fillSelectByName('profile', user.profile);
        this.clickSave();
    },

    clickCreateNew() {
        I.waitForElement(locate('div').withAttr({ title: 'Create a new user' }));
        I.click(locate('div').withAttr({ title: 'Create a new user' }));
    },

    openUserPage() {
        I.wait(1);
        I.waitForElement(locate('a').withAttr({ href: '#/auth' }));
        I.click(locate('a').withAttr({ href: '#/auth' }));
    },

    clickSave() {
        I.click(locate('button').withAttr({ title: 'Save' }));
    },

    clickRemove() {
        I.click(locate('button').withAttr({ title: 'Remove' }));
    },

    clickDiscard() {
        I.click(locate('button').withAttr({ title: 'Discard' }));
    },


    confirmRemove() {
        I.click(locate('button').inside('.confirm-modal').withAttr({ title: 'Remove' }));
    },

    seeHasCreated() {
        I.waitForText('User created.', 20);
    },

    seeHasUpdated() {
        I.waitForText('User updated.', 20);
    },

    seeHasRemoved() {
        I.waitForText('User removed.', 20);
    },

};
