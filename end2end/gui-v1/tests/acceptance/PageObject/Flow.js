let I = actor();

module.exports = {

    init(i) {
        I = i;
    },

    async createDevice() {
        const template = await I.createTemplate({
            label: 'String Template',
            attrs: [
                {
                    label: 'input',
                    type: 'dynamic',
                    value_type: 'string',
                },
                {
                    label: 'output',
                    type: 'dynamic',
                    value_type: 'string',
                },
            ],
        });

        const templateId = template.template.id;

        const device = await I.createDevice({
            templates: [
                templateId,
            ],
            label: 'String device',
        });

        return device.devices[0].id;
    },

    clickOpen() {
        I.click(locate('a').withAttr({ href: '#/flows' }));
    },

    clickCreateNew() {
        I.click(locate('a').withAttr({ href: '#/flows/new' }));
        I.wait(1);
    },

    setFlowName(value) {
        I.fillField('#fld_flowname', value);
    },

    addDeviceInput() {
        I.dragSlider('#palette_node_event_device_in', 300);
    },

    addSwitch() {
        I.click('#palette-collapse-all');
        I.click('#palette-header-function');
        I.dragSlider('#palette_node_switch', 400);
    },

    addChange() {
        I.dragSlider('#palette_node_change', 500);
    },

    addDeviceOutput() {
        I.click('#palette-collapse-all');
        I.click('#palette-header-deprecated_nodes');
        I.dragSlider('#palette_node_device_out', 600);
    },

    addNotification() {
        I.click('#palette-collapse-all');
        I.click('#palette-header-output');
        I.dragSlider('#palette_node_notification', 700);
    },


    async connectFlows() {
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
        I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
        I.dragAndDrop(locate('.port_output').inside(`#${ids[2]}`), locate('.port_input').inside(`#${ids[3]}`));
        I.dragAndDrop(locate(`.port_output`).inside(`#${ids[2]}`), locate(`.port_input`).inside(`#${ids[4]}`));
    },

    clickOnDeviceInput() {
        I.click(`#${ids[0]}`);
        I.doubleClick(`#${ids[0]}`);
    },

    editDeviceInputName() {
        I.fillField('#node-input-name', 'my input');
    },

    selectDevice(deviceId) {
        I.fillField('#node-input-device', `String device (${deviceId})`);
    },

    selectPublish(){
        I.click('#node-input-event_publish');
    },

    clickOnDone() {
        I.click('#node-dialog-ok');
    },

    clickOnSwitch() {
        I.click(`#${ids[1]}`);
        I.doubleClick(`#${ids[1]}`);
    },

    editSwitchProperty() {
        I.fillField('#node-input-property', 'payload.data.attrs.input');
    },

    editSwitchCondition() {
        I.fillField('.node-input-rule-value', 'input value');
    },

    clickOnChange() {
        I.click(`#${ids[2]}`);
        I.doubleClick(`#${ids[2]}`);
    },

    editChangeProperty() {
        I.fillField('.node-input-rule-property-name', 'out.output');
    },

    editChangePropertyValue() {
        I.fillField('.node-input-rule-property-value', 'output value');
    },

    clickOnDeviceOutput() {
        I.click(`#${ids[3]}`);
        I.doubleClick(`#${ids[3]}`);
    },

    editDeviceOutputSource() {
        I.fillField('#node-input-attrs', 'out');
    },

    clickOnNotificationInput() {
        I.click(`#${ids[4]}`);
        I.doubleClick(`#${ids[4]}`);
    },

    editMessageType() {
        I.selectOption('#node-input-msgType', 'Dynamic');
    },

    editMessageDynamicValue() {
        I.fillField('#node-input-messageDynamic', 'out.output');
    },

    editMessageInputSource() {
        I.fillField('#node-input-source', 'out');
    },

    clickOnSave() {
        I.click('.new-btn-circle');
    },

    seeFlowHasCreated() {
        I.wait(1);
        I.see('Flow created.');
    },

    async sendMQTTMessages(deviceId) {
        await I.sendMQTTMessage(deviceId, '{"input": "input value"}');
        await I.sendMQTTMessage(deviceId, '{"input": "input value"}');
    },


};
