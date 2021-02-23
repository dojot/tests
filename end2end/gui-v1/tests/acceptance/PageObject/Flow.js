let I = actor();

module.exports = {

    init(i) {
        I = i;
    },

    async createDevice(deviceName = 'String device') {
        // const template = await I.createTemplate({
        //     label: 'String Template',
        //     attrs: [
        //         {
        //             label: 'input',
        //             type: 'dynamic',
        //             value_type: 'string',
        //         },
        //         {
        //             label: 'output',
        //             type: 'dynamic',
        //             value_type: 'string',
        //         },
        //     ],
        // });

        // const templateId = template.template.id;

        const templateId = await this.createTemplate();
        const device = await I.createDevice({
            templates: [
                templateId,
            ],
            label: deviceName,
        });

        return device.devices[0].id;
    },

    //FLOW TESTE 

async createTemplate(templateName = 'Template') {
    const template = await I.createTemplate({
        label: templateName,
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
    })

    const templateId = template.template.id;
    return templateId;
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

    addMultiActuate() {
        I.click('#palette-collapse-all');
        I.click('#palette-header-output');
        I.dragSlider('#palette_node_multi_actuate', 700);
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

    selectDevice(deviceId, deviceName = 'String device') {
        I.fillField('#node-input-device', `${deviceName} (${deviceId})`);
    },

    selectDeviceTeste(deviceId, deviceName = 'String device') {
        I.fillField('#node-input-device_source_id', `${deviceName} (${deviceId})`);
    },

    selectTemplate(templateId, templateName = 'Template') {
        I.fillField('#node-input-template', `${templateName} (${templateId})`);
    },

    selectTemplateDevice(templateId, templateName = 'Template') {
        I.fillField('#node-input-device-template', `${templateName} (${templateId})`);
    },

    seeSelectTemplateDevice(templateId, templateName = 'Template') {
        I.seeInField('#node-input-device-template', `${templateName} (${templateId})`);
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

    //Fluxo Sanity
    clickFlowCreated(nameFlow){
        I.click(locate('a').withAttr({ href: '#/flows' }));
        I.click(locate('span').withAttr({title: nameFlow}))
        I.wait(3)
    },

    clickRemoveFlow(nameFlow){  
        I.click(locate('span').withAttr({title: nameFlow})) 
        I.click(locate('div').withAttr({ title: 'Remove Flow' }));
        I.click(locate('.confirm-modal button').withAttr({ title: "Remove" }))
        I.wait(3)
    },

    addTemplateIn(){
        I.dragSlider('#palette_node_event_template_in', 200);
    },

    addNodeHTTP(){
        I.dragSlider('#palette_node_http', 400);
    },

    addChange2() {
        I.click('#palette-collapse-all');
        I.click('#palette-header-function');
        I.dragSlider('#palette_node_change', 600);
    },

    addTemplateInFlow() {
        I.click('#palette-collapse-all');
        I.click('#palette-header-deprecated_nodes');
        I.dragSlider('#palette_node_device_template_in', 500)
    },

    addChange3(value) {
        I.click('#palette-collapse-all');
        I.click('#palette-header-function');
        I.dragSlider('#palette_node_change', value);
    },

    addNodeEventDeviceIn1(value){
        I.click('#palette-collapse-all');
        I.click('#palette-header-input');
        I.dragSlider('#palette_node_event_device_in', value);
    },

    addNodeEventDeviceIn(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-input');
        I.dragSlider('#palette_node_event_device_in', 300);
    },

    addFTPRequest(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-output');
        I.dragSlider('#palette_node_ftp', 400)
    },

    addSwitch(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-function');
        I.dragSlider('#palette_node_switch', 600);
    },

    addActuate(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-deprecated_nodes');
        I.dragSlider('#palette_node_actuate', 800)
    },

    addTemplate(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-function');
        I.dragSlider('#palette_node_template', 200);
    },

    addMergeData(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-function');
        I.dragSlider('#palette_node_merge_data', 400);
    },

    addPublishInFTPTopic(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-output');
        I.dragSlider('#palette_node_publish-ftp', 600)
    },

    addCumulativeSum(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-function');
        I.dragSlider('#palette_node_cumulative_sum', 400)
    },

    addCron(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-function');
        I.dragSlider('#palette_node_cron', 300);
    },

    addCronBatch(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-function');
        I.dragSlider('#palette_node_cron-batch', 500) 
    },

    addMultiDeviceOut(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-output');
        I.dragSlider('#palette_node_multi_device_out', 700)
    },

    addGeofence(){
        I.click('#palette-collapse-all');
        //pause();
        I.click('#palette-location')
        I.click('#palette-container-location')
        //I.click('#palette-base-category-location')
        //I.retry(5).click('#palette-header-location');
        I.dragSlider('#palette_node_geofence', 500)
        //I.retry(5).click('#palette-header-location');    
    },

    addGetContext(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-context')
        I.dragSlider('#palette_node_get_context', 600)
    },

    addDeviceIn(){
        I.click('#palette-collapse-all');
        I.click('#palette-header-deprecated_nodes');
        I.dragSlider('#palette_node_device_in', 600)
    },

    seeFlowHasUpdated() {
        I.see('Flow updated.');
        I.wait(1);
    },

    seeFlowRemoved() {
        I.see('Flow removed.');
        I.wait(1);
    },

    //Checking - Fluxo

    seeDeviceEventFlow(deviceId, deviceName = 'String device') {
        I.seeInField('#node-input-device', `${deviceName} (${deviceId})`);
    },

    seeDeviceEventFlowTeste(deviceId, deviceName = 'String device') {
        I.seeInField('#node-input-device_source_id', `${deviceName} (${deviceId})`);
    },

    seeDeviceEventFlowList(deviceId, deviceName = 'String device') {
        I.seeInField('#node-input-list_devices_id', `${deviceName} (${deviceId})`);
    },

    seeFlowTemplateSelect(templateId, templateName = 'Template') {
        I.seeInField('#node-input-template', `${templateName} (${templateId})`);
    },

    seeFlowEventDevice(NameFlow, name, events){
        I.seeInField('#fld_flowname', NameFlow)
        I.seeInField('#node-input-name', name)
        //I.seeInField('ids')
        I.seeCheckboxIsChecked(events)
    },

    seeFlowFTPRequest(method, url, username, password, filename, fileContent, fileEnconding, response, name){
        I.seeInField('#node-input-method', method)
        I.seeInField('#node-input-url', url)
        I.seeInField('#node-input-username', username)
        I.seeInField('#node-input-password', password)
        I.seeInField('#node-input-filename', filename)
        I.seeInField('#node-input-filecontent', fileContent)
        I.seeInField('#node-input-fileencoding', fileEnconding)
        I.seeInField('#node-input-response', response)
        I.seeInField('#node-input-name', name)
    },

    seeFlowSwitch(name, property, value){
        I.seeInField('#node-input-name', name)
        I.seeInField('#node-input-property', property)
        I.seeInField('.node-input-rule-value', value)
    },

    seeFlowMultiActuate(name, source, attrs){
        I.seeInField('#node-input-name', name)
        I.seeInField('#node-input-device_source', source)
        I.seeInField('#node-input-attrs', attrs)
    },

    seeFlowEventDeviceTemplate(Name, name, DeviceTemplate, events){
        I.seeInField('#fld_flowname', Name)
        I.seeInField('#node-input-name', name)
        // falta device id (DeviceTemplate)
    },

    seeFlowHttpRequest(method, url, RequestBody, response, Name){
        I.seeInField('#node-input-method', method)
        I.seeInField('#node-input-url', url)
        I.seeInField('#node-input-body', RequestBody)
        I.seeInField('#node-input-response', response)
        I.seeInField('#node-input-name', Name)
    },

    seeFlowTemplate(Name, SetProperty){
        I.seeInField('#node-input-name', Name)
        I.seeInField('#node-input-field', SetProperty)
    },

    seeFlowNotification(Name, Message, Value, Metadatas){
        I.seeInField('#node-input-name', Name)
        I.seeInField('#node-input-msgType', Message)
        I.seeInField('#node-input-messageStatic', Value)
        I.seeInField('#node-input-source', Metadatas)
    },

    seeFlowEventDevice(NameFlow, Name, Events){
        I.seeInField('#fld_flowname', NameFlow)
        I.seeInField('#node-input-name', Name)
        //Flow.selectDevice(deviceId, 'Event device flow')
        I.seeCheckboxIsChecked(Events)
    },

    seeFlowChange(Name,propertyName, propertyValue){
        I.seeInField('#node-input-name', Name)
        I.seeInField('.node-input-rule-property-name', propertyName)
        I.seeInField('.node-input-rule-property-value', propertyValue)
    },

    seeFlowMergeData(Name, targeData, mergeData){
        I.seeInField('#node-input-name', Name)
        I.seeInField('#node-input-targetData', targeData)
        I.seeInField('#node-input-mergedData', mergeData)
    },

    seeFlowFTP(Name, enconding, fileName, content){
        I.seeInField('#node-input-name', Name)
        I.seeInField('#node-input-encode', enconding)
        I.seeInField('#node-input-filename', fileName)
        I.seeInField('#node-input-filecontent', content)
    },

    seeFlowCron(Name, operation, time, JobName, jobDescription, jobType, jobAction, JobIdentifier){
        I.seeInField('#node-input-name', Name)
        I.seeInField('#node-input-operation', operation)
        I.seeInField('#node-input-cronTimeExpression', time)
        I.seeInField('#node-input-jobName', JobName)
        I.seeInField('#node-input-jobDescription', jobDescription)
        I.seeInField('#node-input-jobType', jobType)
        I.seeInField('#node-input-jobAction', jobAction)
        I.seeInField('#node-input-outJobId', JobIdentifier)
       
    },

    seeFlowCronBatch(Name, operation, jobRequests, JobIdentifier, timeout){
        I.seeInField('#node-input-name', Name)
        I.seeInField('#node-input-operation', operation)
        I.seeInField('#node-input-jobs', jobRequests)
        I.seeInField('#node-input-outJobIds', JobIdentifier)
        I.seeInField('#node-input-timeout', timeout)    
    },

    seeFlowMultiDeviceOut(Name){
        I.seeInField('#node-input-name', Name)
    },

    seeFlowDeviceOut(Name){
        I.seeInField('#node-input-name', Name)
    }



    
};
