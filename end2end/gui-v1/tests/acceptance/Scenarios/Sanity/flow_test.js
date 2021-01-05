Feature('Flow CRUD');

Before((login) => {
    login('admin');
});

Scenario('@flow: Creating a simple flow and publish', async (I, Flow, Device, Notification) => {
    Flow.init(I)
    Flow.clickOpen();

    const deviceId = await Flow.createDevice();

    Flow.clickOpen();
    Flow.clickCreateNew();
    Flow.setFlowName('flow Sanity');
    I.wait(3);
    Flow.addDeviceInput();
    Flow.addSwitch();
    Flow.addChange();
    Flow.addDeviceOutput();
    Flow.addNotification();


    await Flow.connectFlows();

    Flow.clickOnDeviceInput();
    Flow.editDeviceInputName();
    Flow.selectDevice(deviceId);
    Flow.selectPublish();
    Flow.clickOnDone();

    Flow.clickOnSwitch();
    Flow.editSwitchProperty();
    Flow.editSwitchCondition();
    Flow.clickOnDone();

    Flow.clickOnChange();
    Flow.editChangeProperty();
    Flow.editChangePropertyValue();
    Flow.clickOnDone();

    Flow.clickOnDeviceOutput();
    Flow.editDeviceOutputSource();
    Flow.clickOnDone();

    Flow.clickOnNotificationInput();
    Flow.editMessageType();
    Flow.editMessageDynamicValue();
    Flow.editMessageInputSource();
    Flow.clickOnDone();

    Flow.clickOnSave();
    Flow.seeFlowHasCreated();

    Device.openDevicesPage();
    Device.change64QtyToShowPagination();
    Device.clickDetailsDevice(deviceId);
    Device.selectAttr('input');

    await Device.selectAttrSync('output');
    await I.sendMQTTMessage(deviceId, '{"input": "input value"}');
    I.wait(5);

    Device.shouldSeeMessage('output value');

    //await Notification.openNotificationsPage();
    const totalBefore = await Notification.totalOfMessagesWithText('output value');
    await I.sendMQTTMessage(deviceId, '{"input": "input value"}');
    I.wait(5);

    //await Notification.shouldISeeMessagesWithText('output value', totalBefore + 1); 
});

Scenario('@flow: 1° FLOW', async(Flow, I) => {
    Flow.init(I)
    Flow.clickOpen();
    Flow.clickCreateNew();
    Flow.setFlowName('1_FluxoSanity');
    Flow.clickOnSave();
    Flow.clickFlowCreated('1_FluxoSanity');

    //Add caixas 
    Flow.addNodeEventDeviceIn();
    Flow.addFTPRequest();
    Flow.addSwitch();
    Flow.addMultiActuate();

    //conexão
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[2]}`), locate('.port_input').inside(`#${ids[3]}`));

    Flow.clickOnSave();
})

Scenario('@flow: 2° FLOW', async(Flow, I) => {
    Flow.clickOpen();
    Flow.clickCreateNew();
    Flow.setFlowName('2_FluxoSanity');
    Flow.clickOnSave();
    Flow.clickFlowCreated('2_FluxoSanity');

    //Add caixas
    Flow.addTemplateIn();
    Flow.addNodeHTTP();
    Flow.addChange2();
    Flow.addNotification();

    //conexão
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[2]}`), locate('.port_input').inside(`#${ids[3]}`));

    
    Flow.clickOnSave();
})

Scenario('@flow: 3° FLOW', async(Flow, I) => {    
    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('3_FluxoSanity')
    Flow.clickOnSave()
    Flow.seeFlowHasCreated()
    Flow.clickOpen()
    Flow.clickFlowCreated('3_FluxoSanity')
    
    //Add caixas
    Flow.addNodeEventDeviceIn();
    Flow.addTemplate();
    Flow.addMergeData();
    Flow.addPublishInFTPTopic();

    //conexão
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[2]}`), locate('.port_input').inside(`#${ids[3]}`));

    Flow.clickOnSave()
})

Scenario('@flow: 4° FLOW', async(Flow, I) => {    
    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('4_FluxoSanity')
    Flow.clickOnSave()
    Flow.seeFlowHasCreated()
    Flow.clickOpen()
    Flow.clickFlowCreated('4_FluxoSanity')
    
    //Add caixas
    Flow.addTemplateIn();
    Flow.addCumulativeSum();
    Flow.addCron();  
    Flow.addCronBatch();
    Flow.addMultiDeviceOut();

    //conexão
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[2]}`), locate('.port_input').inside(`#${ids[3]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[3]}`), locate('.port_input').inside(`#${ids[4]}`));

    Flow.clickOnSave()
})

// Scenario('@flow: 5° FLOW', async(Flow, I) => {    
//    Flow.clickOpen()
//    Flow.clickCreateNew()
//    Flow.setFlowName('5_FluxoSanity')
//    Flow.clickOnSave()
//    Flow.seeFlowHasCreated()
//    Flow.clickOpen()
//    Flow.clickFlowCreated('5_FluxoSanity')
    
//     // Add caixas
//    Flow.addNodeEventDeviceIn();
//    Flow.addGeofence();
//    Flow.addGetContext();
//    Flow.addDeviceOutput();
//    I.wait(3)

//     //conexão
//     ids = await I.grabAttributeFrom('.nodegroup', 'id');
//     I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
//     I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
//     I.dragAndDrop(locate('.port_output').inside(`#${ids[2]}`), locate('.port_input').inside(`#${ids[3]}`));
//     I.dragAndDrop(locate('.port_output').inside(`#${ids[3]}`), locate('.port_input').inside(`#${ids[4]}`));

//     Flow.clickOnSave()
//     Flow.seeFlowHasCreated();
// })

Scenario('@flow: 6° FLOW', async(Flow, I) => {    
    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('6_FluxoSanity')
    Flow.clickOnSave()
    Flow.seeFlowHasCreated()
    Flow.clickOpen()
    Flow.clickFlowCreated('6_FluxoSanity')
    
    //Add caixas
    Flow.addNodeEventDeviceIn();
    Flow.addTemplate();
    Flow.addSwitch();
    Flow.addDeviceOutput();
   
    //conexão
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[2]}`), locate('.port_input').inside(`#${ids[3]}`));
    
    Flow.clickOnSave()
})

Scenario('@flow: 7° FLOW', async(Flow, I) => {    
    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('7_FluxoSanity')
    Flow.clickOnSave()
    Flow.seeFlowHasCreated()
    Flow.clickOpen()
    Flow.clickFlowCreated('7_FluxoSanity')
    
    //Add caixas
    Flow.addDeviceIn();
    Flow.addChange2();
    Flow.addTemplate();
    Flow.addNotification();

    //conexão
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[2]}`), locate('.port_input').inside(`#${ids[3]}`));
    
    Flow.clickOnSave()
})

Scenario('@flow: REMOVE FLOW', async(Flow) => {
    Flow.clickOpen()
    Flow.clickRemoveFlow('7_FluxoSanity')
    Flow.seeFlowRemoved();
})

Scenario('@flow: UPDATE FLOW', async(Flow) => {
    Flow.clickFlowCreated('6_FluxoSanity')
    Flow.addActuate();
    Flow.clickOnSave()
    Flow.seeFlowHasUpdated();
})