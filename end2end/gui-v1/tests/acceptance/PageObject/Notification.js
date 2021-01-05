const I = actor();

module.exports = {

    async openNotificationsPage() {
        await I.click(locate('a').withAttr({ href: '#/notifications' }));
    },

    shouldSeeMessage(message) {
        I.see(message);
    },

    async totalOfMessagesWithText(text) {
        return await I.grabNumberOfVisibleElements(locate('.info-row .main').withText(text));
    },

    async shouldISeeMessagesWithText(text, total) {
        await I.seeNumberOfVisibleElements(locate('.info-row .main').withText(text), total);
    },

};
