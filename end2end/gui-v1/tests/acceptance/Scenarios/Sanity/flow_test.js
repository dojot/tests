const Flow = require("../../PageObject/Flow");
const { seeFlowEventDevice } = require("../../PageObject/Flow");

Feature('Flow CRUD');

Before((login) => {
    login('admin');
});

Scenario('@flow: 1° FLOW', async(Flow, I) => {
    Flow.init(I);
    const deviceId = await Flow.createDevice('Device-test');

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

    //Configuração
    I.click(`#${ids[0]}`);
    I.doubleClick(`#${ids[0]}`);
    I.fillField('#node-input-name', 'dispositivo')
    Flow.selectDevice(deviceId, 'Device-test')
    I.checkOption('#node-input-event_publish')
    Flow.clickOnDone();

    I.click(`#${ids[1]}`);
    I.doubleClick(`#${ids[1]}`);
    I.selectOption('#node-input-method', 'PUT')
    I.fillField('#node-input-url', 'ftp://10.202.71.0')
    I.fillField('#node-input-username', 'dojot')
    I.fillField('#node-input-password', '1234')
    I.fillField('#node-input-filename', 'data_filename')
    I.fillField('#node-input-filecontent', 'data_content')
    I.fillField('#node-input-fileencoding', 'utf-8')
    I.fillField('#node-input-response', 'ftp_output')
    I.fillField('#node-input-name', 'FTP')
    Flow.clickOnDone();

    I.click(`#${ids[2]}`);
    I.doubleClick(`#${ids[2]}`);
    I.fillField('#node-input-name', 'is true')
    I.fillField('#node-input-property', 'payload.data.attrs.bool')
    I.fillField('.node-input-rule-value', 'is true')
    Flow.clickOnDone();

    I.click(`#${ids[3]}`);
    I.doubleClick(`#${ids[3]}`);
    I.fillField('#node-input-name', 'Test_Flow')
    I.selectOption('#node-input-device_source', 'self')
    I.fillField('#node-input-attrs', 'command')
    Flow.clickOnDone();

    I.wait(2)
    Flow.clickOnSave();
})

Scenario('@flow checking Flow 1°', async (I, Flow) =>{
    Flow.init(I);

    //const deviceId = await Flow.createDevice('Device-test');
    
    Flow.clickOpen();
    Flow.clickFlowCreated('1_FluxoSanity');

    //Event device
    I.click(`#${ids[0]}`);
    I.doubleClick(`#${ids[0]}`);
    Flow.seeFlowEventDevice(
        '1_FluxoSanity', 
        'dispositivo', 
        '#node-input-event_publish')
    //Flow.seeDeviceEventFlow(deviceId, 'Device-test')
    Flow.clickOnDone();    
    
    //FTP request
    I.click(`#${ids[1]}`);
    I.doubleClick(`#${ids[1]}`);
    Flow.seeFlowFTPRequest(
        'PUT',
        'ftp://10.202.71.0',
        'dojot',
        '1234',
        'data_filename',
        'data_content',
        'utf-8',
        'ftp_output',
        'FTP')
    Flow.clickOnDone();

    //Switch
    I.click(`#${ids[2]}`);
    I.doubleClick(`#${ids[2]}`);
    Flow.seeFlowSwitch(
        'is true',
        'payload.data.attrs.bool',
        'is true'
    )    
    Flow.clickOnDone();
    
    //Multi Actuate
    I.click(`#${ids[3]}`);
    I.doubleClick(`#${ids[3]}`);
    Flow.seeFlowMultiActuate(
        'Test_Flow',
        'self',
        'command'
    )
    Flow.clickOnDone();

    I.wait(2)
    Flow.clickOnSave();
})

Scenario('@flow: 2° FLOW', async(Flow, I) => {
    Flow.init(I);
    
    const templateIdFlow = await Flow.createTemplate('Template');

    Flow.clickOpen();
    Flow.clickCreateNew();
    Flow.setFlowName('2_FluxoSanity');
    Flow.clickOnSave();
    Flow.clickFlowCreated('2_FluxoSanity');

    //Add caixas
    Flow.addTemplateIn();
    Flow.addNodeHTTP();
    Flow.addTemplate();
    Flow.addNotification();
    

    //conexão
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[2]}`), locate('.port_input').inside(`#${ids[3]}`));

    //configurações
    I.click(`#${ids[0]}`);
    I.doubleClick(`#${ids[0]}`); 
    I.fillField('#node-input-name', 'Teste de nó')
    Flow.selectTemplate(templateIdFlow, 'Template')
    I.checkOption('#node-input-event_publish')
    Flow.clickOnDone();

    I.click(`#${ids[1]}`);
    I.doubleClick(`#${ids[1]}`);
    I.fillField('#node-input-url', 'http://ptsv2.com/t/3fbhu-1543424220/post')
    I.fillField('#node-input-body', 'reqBody')
    I.fillField('#node-input-response', 'responseGET')
    I.fillField('#node-input-name', 'http-Test')
    Flow.clickOnDone();

    I.click(`#${ids[2]}`);
    I.doubleClick(`#${ids[2]}`);
    I.fillField('#node-input-name', 'Template-Test')
    I.fillField('#node-input-field', 'reqBody')
   // I.selectOption('.fa-code', 'Plain Text')
    I.clearField('.ace_text-input')
    I.fillField('.ace_text-input', '{"payload": "valor do atributo: {{payload.data.attrs.chuva}}"}')
    Flow.clickOnDone();

    I.click(`#${ids[3]}`);
    I.doubleClick(`#${ids[3]}`);
    I.fillField('#node-input-name', 'Notification_Flow')
    I.selectOption('#node-input-msgType', 'static')
    I.fillField('#node-input-messageStatic', 'test')
    I.fillField('#node-input-source', 'out')
    Flow.clickOnDone();
    
    I.wait(2)
    Flow.clickOnSave();
})

Scenario('@flow checking Flow 2°', async (I, Flow) =>{
        Flow.init(I);

        const templateIdFlow = await Flow.createTemplate('Template');
        
        Flow.clickOpen();
        Flow.clickFlowCreated('2_FluxoSanity');
    
        //Event Device Template
        I.click(`#${ids[0]}`);
        I.doubleClick(`#${ids[0]}`);
        Flow.seeFlowEventDeviceTemplate(
            '2_FluxoSanity', 
            'Teste de nó', 
            '#node-input-event_publish')
        //Flow.seeFlowTemplateSelect(templateIdFlow)
        Flow.clickOnDone();    

        
        //Http request
        I.click(`#${ids[1]}`);
        I.doubleClick(`#${ids[1]}`);
        Flow.seeFlowHttpRequest(
            'GET',
            'http://ptsv2.com/t/3fbhu-1543424220/post',
            'reqBody',
            'responseGET',
            'http-Test'
        )
        Flow.clickOnDone();
    
        //Template
        I.click(`#${ids[2]}`);
        I.doubleClick(`#${ids[2]}`);
        Flow.seeFlowTemplate(
            'Template-Test',
            'reqBody',
            //'Plain text',
            //'{"payload": "valor do atributo: {{payload.data.attrs.chuva}}"}'
        )
                
        Flow.clickOnDone();
        
        //Notification
        I.click(`#${ids[3]}`);
        I.doubleClick(`#${ids[3]}`);
        Flow.seeFlowNotification(
            'Notification_Flow',
            'static',
            'test',
            'out'
        )
        Flow.clickOnDone();

        I.wait(2)
    Flow.clickOnSave();
    })

Scenario('@flow: 3° FLOW', async(Flow, I) => {    
    Flow.init(I)

    const deviceId = await Flow.createDevice('Event device flow');
   
    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('3_FluxoSanity')
    Flow.clickOnSave()
    Flow.seeFlowHasCreated()
    Flow.clickOpen()
    Flow.clickFlowCreated('3_FluxoSanity')
    
    //Add caixas
    Flow.addNodeEventDeviceIn();
    Flow.addChange2(); 
    Flow.addMergeData();
    Flow.addPublishInFTPTopic();

    //conexão
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[2]}`), locate('.port_input').inside(`#${ids[3]}`));

    //Configurações
    I.click(`#${ids[0]}`);
    I.doubleClick(`#${ids[0]}`);
    I.fillField('#node-input-name', 'device')
    Flow.selectDevice(deviceId, 'Event device flow')
    I.checkOption('#node-input-event_publish')
    Flow.clickOnDone();

    I.click(`#${ids[1]}`);
    I.doubleClick(`#${ids[1]}`);
    I.fillField('#node-input-name', 'Test_Flow')
    I.fillField('.node-input-rule-type', 'Set')
    I.fillField('.node-input-rule-property-name', 'saida.teste')
    I.fillField('.node-input-rule-property-value', 'teste')
    Flow.clickOnDone();

    I.click(`#${ids[2]}`);
    I.doubleClick(`#${ids[2]}`);
    I.fillField('#node-input-name', 'MergeData')
    I.fillField('#node-input-targetData', 'out')
    I.fillField('#node-input-mergedData', 'mergedData')
    Flow.clickOnDone();

    I.click(`#${ids[3]}`);
    I.doubleClick(`#${ids[3]}`);
    I.fillField('#node-input-name', 'FTP')
    I.fillField('#node-input-encode', 'utf8')
    I.fillField('#node-input-filename', 'data_filenameut')
    I.fillField('#node-input-filecontent', 'data_content')
    Flow.clickOnDone();

    I.wait(2)
    Flow.clickOnSave();
})

Scenario('@flow checking Flow 3°', async (I, Flow) =>{
        Flow.init(I);
    
        Flow.clickOpen();
        Flow.clickFlowCreated('3_FluxoSanity');
    
        //Event Device Template
        I.click(`#${ids[0]}`);
        I.doubleClick(`#${ids[0]}`);
        Flow.seeFlowEventDeviceTemplate(
            '3_FluxoSanity', 
            'device', 
            '#node-input-event_publish')
        Flow.clickOnDone();    
        
        //Change
        I.click(`#${ids[1]}`);
        I.doubleClick(`#${ids[1]}`);
        Flow.seeFlowChange(
            'Test_Flow',
            'saida.teste',
            'teste'
        )
        Flow.clickOnDone();
    
        //Merge Data
        I.click(`#${ids[2]}`);
        I.doubleClick(`#${ids[2]}`);
        Flow.seeFlowMergeData(
            'MergeData',
            'out',
            'mergedData',
        )    
        Flow.clickOnDone();
        
        //Publish in FTP topic
        I.click(`#${ids[3]}`);
        I.doubleClick(`#${ids[3]}`);
        Flow.seeFlowFTP(
            'FTP',
            'utf8',
            'data_filenameut',
            'data_content'
        )
        Flow.clickOnDone();

        I.wait(2)
        Flow.clickOnSave();
    })

Scenario('@flow: 4° FLOW', async(Flow, I) => { 
    Flow.init(I);
    
    const templateIdFlow = await Flow.createTemplate('flow-template');

    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('4_FluxoSanity')
    Flow.clickOnSave()
    Flow.seeFlowHasCreated()
    Flow.clickOpen()
    Flow.clickFlowCreated('4_FluxoSanity')
    
    //Add caixas
    Flow.addTemplateIn();
    Flow.addCron();  
    Flow.addCronBatch();
    Flow.addMultiDeviceOut();

    //conexão
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[2]}`), locate('.port_input').inside(`#${ids[3]}`));

    //configuração
    I.click(`#${ids[0]}`);
    I.doubleClick(`#${ids[0]}`);
    I.fillField('#node-input-name', 'Event device template')
    Flow.selectTemplate(templateIdFlow, 'flow-template')
    I.checkOption('#node-input-event_publish')
    Flow.clickOnDone();

    I.click(`#${ids[1]}`);
    I.doubleClick(`#${ids[1]}`);
    I.fillField('#node-input-name', 'create')
    I.fillField('#node-input-operation', 'CREATE')
    I.fillField('#node-input-cronTimeExpression', '*/2 * * * *')
    I.fillField('#node-input-jobName', 'keepalive2')
    I.fillField('#node-input-jobDescription', 'Esse job envia notificação de keepalive2 a cada 2 minutos')
    I.fillField('#node-input-jobType', 'EVENT REQUEST')
    I.fillField('#node-input-jobAction', 'jobAction')
    I.fillField('#node-input-outJobId', 'out.jobID')
    Flow.clickOnDone();

    I.click(`#${ids[2]}`);
    I.doubleClick(`#${ids[2]}`);
    I.fillField('#node-input-name', 'cron-batch')
    I.fillField('#node-input-operation', 'CREATE')
    I.fillField('#node-input-jobs', 'reqJOB')
    I.fillField('#node-input-outJobIds', 'out.job_id')
    I.fillField('#node-input-timeout', '1000')
    Flow.clickOnDone();

    I.click(`#${ids[3]}`);
    I.doubleClick(`#${ids[3]}`);
    I.fillField('#node-input-name', 'multi device')
    I.fillField('#node-input-device_source', 'The device which triggered the flow')
    I.fillField('#node-input-attrs', 'command')
    Flow.clickOnDone();
    
    I.wait(2)
    Flow.clickOnSave();
})

Scenario('@flow checking Flow 4°', async (I, Flow) =>{
        Flow.init(I);
    
        Flow.clickOpen();
        Flow.clickFlowCreated('4_FluxoSanity');
    
        //Event device template
        I.click(`#${ids[0]}`);
        I.doubleClick(`#${ids[0]}`);
        Flow.seeFlowEventDeviceTemplate(
            '4_FluxoSanity', 
            'Event device template',
            //selecionar o template ID 
            '#node-input-event_remove')
        Flow.clickOnDone();    
        
        //Cron
        I.click(`#${ids[1]}`);
        I.doubleClick(`#${ids[1]}`);
        Flow.seeFlowCron(
            'create',
            'CREATE',
            '*/2 * * * *',
            'keepalive2',
            'Esse job envia notificação de keepalive2 a cada 2 minutos',
            'EVENT REQUEST',
            'jobAction',
            'out.jobID'
        )
        Flow.clickOnDone();
    
        //Cron Batch
        I.click(`#${ids[2]}`);
        I.doubleClick(`#${ids[2]}`);
        Flow.seeFlowCronBatch(
            'cron-batch',
            'CREATE',
            'reqJOB',
            'out.job_id',
            '1000'
        )    
        Flow.clickOnDone();
        
        //Multi device out
        I.click(`#${ids[3]}`);
        I.doubleClick(`#${ids[3]}`);
        Flow.seeFlowMultiDeviceOut(
            'multi device',
        )
        I.seeInField('#node-input-attrs', 'command')
        Flow.clickOnDone();

        I.wait(2)
        Flow.clickOnSave();
    })

Scenario('@flow: 5° FLOW', async(Flow, I) => {  
    Flow.init(I)

    const deviceId = await Flow.createDevice('Event'); 

    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('5_FluxoSanity')
    Flow.clickOnSave()
    Flow.seeFlowHasCreated()
    Flow.clickOpen()
    Flow.clickFlowCreated('5_FluxoSanity')
    
    //Add caixas
    Flow.addNodeEventDeviceIn();
    Flow.addTemplate();
    Flow.addDeviceOutput();
   
    //conexão
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.dragAndDrop(locate('.port_output').inside(`#${ids[0]}`), locate('.port_input').inside(`#${ids[1]}`));
    I.dragAndDrop(locate('.port_output').inside(`#${ids[1]}`), locate('.port_input').inside(`#${ids[2]}`));
    
    //configuração
    I.click(`#${ids[0]}`);
    I.doubleClick(`#${ids[0]}`);
    I.fillField('#node-input-name', 'Event device')
    Flow.selectDevice(deviceId, 'Event')
    I.checkOption('#node-input-event_configure')
    Flow.clickOnDone();

    I.click(`#${ids[1]}`);
    I.doubleClick(`#${ids[1]}`);
    I.fillField('#node-input-name', 'filename')
    I.fillField('#node-input-field', 'data.filename')
    I.fillField('#node-input-syntax', 'Handlebars template')
    I.clearField('.ace_text-input')
    I.fillField('.ace_text-input', 'test123456')
    Flow.clickOnDone();

    I.click(`#${ids[2]}`);
    I.doubleClick(`#${ids[2]}`);
    I.fillField('#node-input-name', 'device out')
    I.fillField('#node-input-device_source', 'The device which triggered the flow')
    I.fillField('#node-input-attrs', 'teste')
    Flow.clickOnDone();

    I.wait(2)
    Flow.clickOnSave();
})

Scenario('@flow checking Flow 5°', async (I, Flow) =>{
        Flow.init(I);
    
        Flow.clickOpen();
        Flow.clickFlowCreated('5_FluxoSanity');
    
        //Event device 
        I.click(`#${ids[0]}`);
        I.doubleClick(`#${ids[0]}`);
        Flow.seeFlowEventDevice(
            '5_FluxoSanity', 
            'Event device',
            //DEVICE ID
            '#node-input-event_configure')
        Flow.clickOnDone();    
        
        //Template
        I.click(`#${ids[1]}`);
        I.doubleClick(`#${ids[1]}`);
        Flow.seeFlowTemplate(
           'filename',
           'data.filename',
        )
        I.seeElement('#node-input-template-editor', 'test123456')
        Flow.clickOnDone();
    
        //Device out
        I.click(`#${ids[2]}`);
        I.doubleClick(`#${ids[2]}`);
        Flow.seeFlowDeviceOut(
            'device out'
        )    
        I.seeElement('#node-input-device_source', 'The device which triggered the flow')
        I.seeInField('#node-input-attrs', 'teste')
        Flow.clickOnDone();

        I.wait(2)
        Flow.clickOnSave();
    })


    ///////// Configurações Avulsas dos nós /////////

    

    Scenario('@flow Event Device ', async (Flow, I) => {
        Flow.init(I);
        const deviceId = await Flow.createDevice('Event device');

        Flow.clickOpen()
        Flow.clickCreateNew()
        Flow.setFlowName('Event device - Actuation')
        Flow.addNodeEventDeviceIn1(200)
    
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`)

        I.fillField('#node-input-name', 'Event device')
        I.checkOption('#node-input-event_configure')
        Flow.selectDevice(deviceId, 'Event device')
        Flow.clickOnDone();

        Flow.clickOnSave()    
    })

    Scenario('@flow Checking - Event Device ', async (Flow, I) => {
        Flow.init(I);
        const deviceId = await Flow.createDevice('Event device flow');

        Flow.clickOpen()
        Flow.clickFlowCreated('Event device - Actuation')
    
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`)

        I.seeInField('#node-input-name', 'Event device')
        //Flow.seeDeviceEventFlow(deviceId, 'Event device')
        I.seeCheckboxIsChecked('#node-input-event_configure')
        Flow.clickOnDone();

        I.wait(2)
        Flow.clickOnSave();    
    })

                
        Scenario('@flow  Event device template - create', async (Flow, I) => {
        Flow.init(I);
                    
        const templateIdFlow = await Flow.createTemplate('event device template - create');
                    
        Flow.clickOpen();
        Flow.clickCreateNew();
        Flow.setFlowName('Event device template');
        Flow.clickOnSave();
        Flow.clickFlowCreated('Event device template');
                    
        I.dragSlider('#palette_node_event_template_in', 400);

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Event Device - create')
        Flow.selectTemplate(templateIdFlow, 'event device template - create')
        I.checkOption('#node-input-event_create')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave() 
                        
        })

        Scenario('@flow Checking - Event device template - create', async (Flow, I) => {
        Flow.init(I);

        const templateIdFlow = await Flow.createTemplate('event device template - create');
                        
        Flow.clickOpen();
        Flow.clickFlowCreated('Event device template');
                        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        Flow.seeFlowEventDeviceTemplate(
            'Event device template', 
            'Event Device - create', 
            '#node-input-event_create'
        )
        //Flow.seeFlowTemplateSelect(templateIdFlow, 'event device template - create')
        Flow.clickOnDone(); 
                        
        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  Event device template - update', async (Flow, I) => {
        Flow.init(I);

        const templateIdFlow = await Flow.createTemplate('event device template - update');
   
        Flow.clickOpen()
        Flow.clickFlowCreated('Event device template');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Event Device - update')
        Flow.selectTemplate(templateIdFlow, 'event device template - update')
        I.uncheckOption('#node-input-event_create')
        I.checkOption('#node-input-event_update')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()

    })

    Scenario('@flow Checking - Event device template - update', async (Flow, I) => {
        Flow.clickOpen();

        const templateIdFlow = await Flow.createTemplate('event device template - update');

        Flow.clickFlowCreated('Event device template');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        Flow.seeFlowEventDeviceTemplate(
            'Event device template', 
            'Event Device - update',
            '#node-input-event_update')
        //Flow.seeFlowTemplateSelect(templateIdFlow, 'event device template - update')
        Flow.clickOnDone(); 

        I.wait(3)
        Flow.clickOnSave()
    })


    Scenario('@flow  Event device template - remove', async (Flow, I) => {
        Flow.init(I);

        const templateIdFlow = await Flow.createTemplate('event device template - remove');
   
        Flow.clickOpen()
        Flow.clickFlowCreated('Event device template');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Event Device - remove')
        Flow.selectTemplate(templateIdFlow, 'event device template - remove')
        I.uncheckOption('#node-input-event_update')
        I.checkOption('#node-input-event_remove')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()


    })

    Scenario('@flow Checking - Event device template - remove', async (Flow, I) => {
        Flow.clickOpen();

        const templateIdFlow = await Flow.createTemplate('event device template - remove');

        Flow.clickFlowCreated('Event device template');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        Flow.seeFlowEventDeviceTemplate(
            'Event device template', 
            'Event Device - remove',
            '#node-input-event_remove')
        //Flow.seeFlowTemplateSelect(templateIdFlow, 'event device template - update')
        Flow.clickOnDone(); 

        I.wait(3)
        Flow.clickOnSave()
    })
   
    Scenario('@flow  Event device template - actuate', async (Flow, I) => {
        Flow.init(I);

        const templateIdFlow = await Flow.createTemplate('event device template - actuate');
   
        Flow.clickOpen()
        Flow.clickFlowCreated('Event device template');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Event Device - actuate')
        Flow.selectTemplate(templateIdFlow, 'event device template - actuate')
        I.uncheckOption('#node-input-event_remove')
        I.checkOption('#node-input-event_configure')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()


    })

    Scenario('@flow Checking - Event device template - actuate', async (Flow, I) => {
        Flow.clickOpen();

        const templateIdFlow = await Flow.createTemplate('event device template - actuate');

        Flow.clickFlowCreated('Event device template');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        Flow.seeFlowEventDeviceTemplate(
            'Event device template', 
            'Event Device - actuate',
            '#node-input-event_configure')
        //Flow.seeFlowTemplateSelect(templateIdFlow, 'event device template - update')
        Flow.clickOnDone(); 

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  Event device template - ALL', async (Flow, I) => {
        Flow.init(I);

        const templateIdFlow = await Flow.createTemplate('event device template - actuate');
   
        Flow.clickOpen()
        Flow.clickFlowCreated('Event device template');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Event Device - ALL')
        Flow.selectTemplate(templateIdFlow, 'event device template - ALL')
        I.uncheckOption('#node-input-event_configure')
        I.checkOption('#node-input-event_create')
        I.checkOption('#node-input-event_update')
        I.checkOption('#node-input-event_remove')
        I.checkOption('#node-input-event_configure')
        I.checkOption('#node-input-event_publish')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()


    })

    Scenario('@flow Checking - Event device template - ALL', async (Flow, I) => {
        Flow.clickOpen();

        const templateIdFlow = await Flow.createTemplate('event device template - ALL');

        Flow.clickFlowCreated('Event device template');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'Event Device - ALL')
        //template id <- falta
        I.seeCheckboxIsChecked('#node-input-event_create') 
        I.seeCheckboxIsChecked('#node-input-event_update')
        I.seeCheckboxIsChecked('#node-input-event_remove')
        I.seeCheckboxIsChecked('#node-input-event_configure')
        I.seeCheckboxIsChecked('#node-input-event_publish')

        //Flow.seeFlowTemplateSelect(templateIdFlow, 'event device template - update')
        Flow.clickOnDone(); 

        I.wait(3)
        Flow.clickOnSave()
    })

    ///////HTTP REQUEST////
    Scenario('@flow  HTTP Request - POST', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickCreateNew();
        Flow.setFlowName('HTTP Request');
        Flow.clickOnSave();
        Flow.clickFlowCreated('HTTP Request');
                    
        I.dragSlider('#palette_node_http', 400);

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.selectOption('#node-input-method', 'POST')
        I.fillField('#node-input-url', 'http://test.com')
        I.fillField('#node-input-body', 'reqBody')
        I.fillField('#node-input-response', 'responsePOST')
        I.fillField('#node-input-name', 'http-POST')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - HTTP Request - POST', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('HTTP Request');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        Flow.seeFlowHttpRequest(
            'POST',
            'http://test.com',
            'reqBody',
            'responsePOST',
            'http-POST'
            )
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  HTTP Request - DELETE', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickFlowCreated('HTTP Request');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.selectOption('#node-input-method', 'DELETE')
        I.fillField('#node-input-url', 'http://test.com/delete')
        I.fillField('#node-input-body', 'reqBody')
        I.fillField('#node-input-response', 'responseDELETE')
        I.selectOption('#node-input-ret', 'bin')
        I.fillField('#node-input-name', 'http-DELETE')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - HTTP Request - DELETE', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('HTTP Request');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        Flow.seeFlowHttpRequest(
            'DELETE',
            'http://test.com/delete',
            'reqBody',
            'responseDELETE',
            'http-DELETE'
            )
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  HTTP Request - GET', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickFlowCreated('HTTP Request');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.selectOption('#node-input-method', 'GET')
        I.fillField('#node-input-url', 'http://test.com/get')
        I.fillField('#node-input-body', 'reqBody')
        I.fillField('#node-input-response', 'responseGET')
        I.selectOption('#node-input-ret', 'obj')
        I.fillField('#node-input-name', 'http-GET')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - HTTP Request - GET', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('HTTP Request');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        Flow.seeFlowHttpRequest(
            'GET',
            'http://test.com/get',
            'reqBody',
            'responseGET',
            'http-GET'
            )
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    
    Scenario('@flow  HTTP Request - -set by msg-method-', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickFlowCreated('HTTP Request');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.selectOption('#node-input-method', 'use')
        I.fillField('#node-input-url', 'http://test.com/setbymsg-method')
        I.fillField('#node-input-body', 'reqBody')
        I.fillField('#node-input-response', 'responseMSG')
        I.fillField('#node-input-name', 'http-set by msg-method-')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - HTTP Request - -set by msg-method-', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('HTTP Request');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        //I.seeInField('#node-input-method', '')
        I.seeInField('#node-input-url', 'http://test.com/setbymsg-method')
        I.seeInField('#node-input-body', 'reqBody')
        I.seeInField('#node-input-response', 'responseMSG')
        I.seeInField('#node-input-name', 'http-set by msg-method-')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

     ///////MULTI DEVICE OUT////
    Scenario('@flow  Multi Device Out', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickCreateNew();
        Flow.setFlowName('multi device out');
        Flow.clickOnSave();
        Flow.clickFlowCreated('multi device out');
                    
        Flow.addMultiDeviceOut()

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'multi device out')
        I.selectOption('#node-input-device_source', 'dynamic')
        I.fillField('#node-input-devices_source_dynamic', 'saida')
        I.fillField('#node-input-attrs', 'command')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Multi Device Out', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('multi device out');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'multi device out')
        //I.seeInField('#node-input-device_source', 'Device(s) defined during the flow')
        I.seeInField('#node-input-devices_source_dynamic', 'saida')
        I.seeInField('#node-input-attrs', 'command')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  Multi Device Out - Specific device(s)', async (Flow, I) => {
        Flow.init(I);
        
        const deviceId = await Flow.createDevice('Multi');
                    
        Flow.clickOpen();
        Flow.clickFlowCreated('multi device out');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Specific device(s)')
        I.selectOption('#node-input-device_source', 'configured')
        Flow.selectDeviceTeste(deviceId, 'Multi')
        I.fillField('#node-input-attrs', 'command')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Multi Device Out - Specific device(s)', async (Flow, I) => {
        Flow.clickOpen();

        const deviceId = await Flow.createDevice('Multi');

        Flow.clickFlowCreated('multi device out');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'Specific device(s)')
        //Flow.seeDeviceEventFlowTeste(deviceId, 'Multi')
        I.seeInField('#node-input-attrs', 'command')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    //////PUBLISH FTP////
    Scenario('@flow  Publish FTP - ascii ', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickCreateNew();
        Flow.setFlowName('Publish FTP');
        Flow.clickOnSave();
        Flow.clickFlowCreated('Publish FTP');
                    
        Flow.addPublishInFTPTopic()

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Publish FTP - ascii')
        I.selectOption('#node-input-encode', 'ascii')
        I.fillField('#node-input-filename', 'saida')
        I.fillField('#node-input-filecontent', 'ftp')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Publish FTP - ascii', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('Publish FTP');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'Publish FTP - ascii')
        //I.selectOption('#node-input-encode', 'ascii')
        I.seeInField('#node-input-filename', 'saida')
        I.seeInField('#node-input-filecontent', 'ftp')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  Publish FTP - base64 ', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickFlowCreated('Publish FTP');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Publish FTP - base64')
        I.selectOption('#node-input-encode', 'base64')
        I.fillField('#node-input-filename', 'saida')
        I.fillField('#node-input-filecontent', 'base64')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Publish FTP - base64', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('Publish FTP');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'Publish FTP - base64')
        //I.selectOption('#node-input-encode', 'base64')
        I.seeInField('#node-input-filename', 'saida')
        I.seeInField('#node-input-filecontent', 'base64')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  Publish FTP - hex ', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickFlowCreated('Publish FTP');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Publish FTP - hex')
        I.selectOption('#node-input-encode', 'hex')
        I.fillField('#node-input-filename', 'entrada')
        I.fillField('#node-input-filecontent', 'hex')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Publish FTP - hex', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('Publish FTP');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'Publish FTP - hex')
        //I.selectOption('#node-input-encode', 'hex')
        I.seeInField('#node-input-filename', 'entrada')
        I.seeInField('#node-input-filecontent', 'hex')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  Publish FTP - utf16le ', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickFlowCreated('Publish FTP');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Publish FTP - utf16le')
        I.selectOption('#node-input-encode', 'utf16le')
        I.fillField('#node-input-filename', 'entrada')
        I.fillField('#node-input-filecontent', 'utf16le')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Publish FTP - utf16le', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('Publish FTP');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'Publish FTP - utf16le')
        //I.selectOption('#node-input-encode', 'utf16le')
        I.seeInField('#node-input-filename', 'entrada')
        I.seeInField('#node-input-filecontent', 'utf16le')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  Publish FTP - utf8 ', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickFlowCreated('Publish FTP');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Publish FTP - utf8')
        I.selectOption('#node-input-encode', 'utf8')
        I.fillField('#node-input-filename', 'entrada')
        I.fillField('#node-input-filecontent', 'utf8')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Publish FTP - utf8', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('Publish FTP');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'Publish FTP - utf8')
        //I.selectOption('#node-input-encode', 'utf8')
        I.seeInField('#node-input-filename', 'entrada')
        I.seeInField('#node-input-filecontent', 'utf8')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

        Scenario('@flow  Publish FTP - utf8 ', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickFlowCreated('Publish FTP');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Publish FTP - utf8')
        I.selectOption('#node-input-encode', 'utf8')
        I.fillField('#node-input-filename', 'entrada')
        I.fillField('#node-input-filecontent', 'utf8')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Publish FTP - utf8', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('Publish FTP');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'Publish FTP - utf8')
        //I.selectOption('#node-input-encode', 'utf8')
        I.seeInField('#node-input-filename', 'entrada')
        I.seeInField('#node-input-filecontent', 'utf8')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    //////NOTIFICATION////
    Scenario('@flow  Notification static', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickCreateNew();
        Flow.setFlowName('Notification');
        Flow.clickOnSave();
        Flow.clickFlowCreated('Notification');
                    
        Flow.addNotification()

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Notification - Static')
        I.selectOption('#node-input-msgType', 'static')
        I.fillField('#node-input-messageStatic', '10')
        I.fillField('#node-input-source', 'saida.static')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Notification static', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('Notification');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'Notification - Static')
        //I.seeInField('#node-input-msgType', 'static')
        I.seeInField('#node-input-messageStatic', '10')
        I.seeInField('#node-input-source', 'saida.static')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  Notification dynamic', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickFlowCreated('Notification');
                    
        Flow.addNotification()

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'Notification - Dynamic')
        I.selectOption('#node-input-msgType', 'dynamic')
        I.fillField('#node-input-messageDynamic', 'teste')
        I.fillField('#node-input-source', 'saida.dynamic')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Notification dynamic', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('Notification');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'Notification - Dynamic')
        //I.seeInField('#node-input-msgType', 'static')
        I.seeInField('#node-input-messageDynamic', 'teste')
        I.seeInField('#node-input-source', 'saida.dynamic')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    //////MULTI ACTUATE////
    Scenario('@flow  Multi Actuate', async (Flow, I) => {
        Flow.init(I);
                    
        Flow.clickOpen();
        Flow.clickCreateNew();
        Flow.setFlowName('Multi Actuate');
        Flow.clickOnSave();
        Flow.clickFlowCreated('Multi Actuate');
                    
        Flow.addMultiActuate()

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'MultiActuate - The device which triggered the flow')
        I.selectOption('#node-input-device_source', 'self')
        I.fillField('#node-input-attrs', 'saida.attrs')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Multi Actuate', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('Multi Actuate');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#fld_flowname', 'Multi Actuate')
        I.seeInField('#node-input-name', 'MultiActuate - The device which triggered the flow')
        //I.seeInFiled('#node-input-device_source', 'self')
        I.seeInField('#node-input-attrs', 'saida.attrs')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  Multi Actuate', async (Flow, I) => {
        Flow.init(I);
    
        const deviceId = await Flow.createDevice('Device-test');

        Flow.clickOpen();
        Flow.clickFlowCreated('Multi Actuate');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'MultiActuate - Specific device')
        I.selectOption('#node-input-device_source', 'configured')
        Flow.selectDeviceTeste(deviceId, 'Device-test')
        I.fillField('#node-input-attrs', 'saida.attrs')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Multi Actuate', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('Multi Actuate');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'MultiActuate - Specific device')
        //I.seeInFiled('#node-input-device_source', 'self')
        I.seeInField('#node-input-attrs', 'saida.attrs')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow  Multi Actuate', async (Flow, I) => {
        Flow.init(I);
    
        const deviceId = await Flow.createDevice('Device-test');

        Flow.clickOpen();
        Flow.clickFlowCreated('Multi Actuate');

        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.fillField('#node-input-name', 'MultiActuate - Device(s) defined during the flow')
        I.selectOption('#node-input-device_source', 'dynamic')
        I.fillField('#node-input-devices_source_dynamic', 'test')
        I.fillField('#node-input-attrs', 'saida.test')
        Flow.clickOnDone();

        I.wait(3)
        Flow.clickOnSave()
    })

    Scenario('@flow Checking - Multi Actuate', async (Flow, I) => {
        Flow.clickOpen();

        Flow.clickFlowCreated('Multi Actuate');
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`);

        I.seeInField('#node-input-name', 'MultiActuate - Device(s) defined during the flow')
        //I.seeInFiled('#node-input-device_source', 'dynamic')
        I.seeInField('#node-input-devices_source_dynamic', 'test')
        I.seeInField('#node-input-attrs', 'saida.test')
        Flow.clickOnDone();
    
        I.wait(3)
        Flow.clickOnSave()
    })
    
    //////Change////
  Scenario('@flow Change - String', async (Flow, I) => {
        Flow.clickOpen()
        Flow.clickCreateNew()
        Flow.setFlowName('Change')

        Flow.addChange3(200)
    
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`)

        I.fillField('#node-input-name', 'change-string')
        I.fillField('.node-input-rule-property-name', 'saida.texto')
        I.fillField('.node-input-rule-property-value', 'test')
        Flow.clickOnDone();

        I.wait(1)
        Flow.clickOnSave()    
    })

    Scenario('@flow checking - Change - String', async(I, Flow) => {
        Flow.clickOpen()  
        Flow.clickFlowCreated('Change')
        
        ids = await I.grabAttributeFrom('.nodegroup', 'id');
        I.click(`#${ids}`);
        I.doubleClick(`#${ids}`)

        I.seeInField('#fld_flowname', 'Change')
        I.seeInField('#node-input-name', 'change-string')
        I.seeInField('.node-input-rule-property-name', 'saida.texto')
        I.seeInField('.node-input-rule-property-value', 'test')

        I.wait(1)
        Flow.clickOnSave()
    })

    // Scenario('@flow Change - Number', async (Flow, I) => {
    //     Flow.clickOpen()  
    //     Flow.clickFlowCreated('Change')
    
    //     ids = await I.grabAttributeFrom('.nodegroup', 'id');
    //     I.click(`#${ids}`);
    //     I.doubleClick(`#${ids}`)

    //     I.fillField('#node-input-name', 'change-number')
    //     I.fillField('.node-input-rule-property-name', 'saida.texto')
    //     I.click('.fa-sort-desc')
    //     I.selectOption('.red-ui-typedInput-options', 'num')
    //     I.fillField('.node-input-rule-property-value', '50')
    //     Flow.clickOnDone();

    //     I.wait(2)
    //     Flow.clickOnSave()    
    // })

    // Scenario('@flow checking - Change - Number', async(I, Flow) => {
    //     Flow.clickOpen()  
    //     Flow.clickFlowCreated('Change')
        
    //     ids = await I.grabAttributeFrom('.nodegroup', 'id');
    //     I.click(`#${ids}`);
    //     I.doubleClick(`#${ids}`)

    //     I.seeInField('#fld_flowname', 'Change')
    //     I.seeInField('#node-input-name', 'change-string')
    //     I.seeInField('.node-input-rule-property-name', 'saida.texto')
    //     I.seeInField('.node-input-rule-property-value', 'test')
    //     Flow.clickOnDone();
        
    //     I.wait(1)
    //     Flow.clickOnSave()  
    // })

//////TEMPLATE///////
Scenario('@flow Template', async (Flow, I) => {
    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('Template')

    Flow.addTemplate()

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'template - Mustache template (deprecated)')
    I.selectOption('#node-input-syntax', 'mustache')
    I.clearField('.ace_text-input')
    I.fillField('.ace_text-input', '{"payload": "valor do atributo: {{payload.data.attrs.teste}}"}')
    I.selectOption('#node-input-output', 'str')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()    
})

Scenario('@flow checking - Template', async(I, Flow) => {
    Flow.clickOpen()  
    Flow.clickFlowCreated('Template')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'template - Mustache template (deprecated)')
    //I.selectOption('#node-input-syntax', 'plain')
    //I.seeInField('.ace_text-input', '{"payload": "valor do atributo: {{payload.data.attrs.teste}}"}')
    I.seeInField('#node-input-output', 'str')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()
})

Scenario('@flow Template', async (Flow, I) => {
    Flow.clickOpen()  
    Flow.clickFlowCreated('Template')

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'template - Plain text - Json')
    I.selectOption('#node-input-syntax', 'plain')
    I.clearField('.ace_text-input')
    I.fillField('.ace_text-input', '{"payload": "valor: {{payload.data.attrs.teste}}"}')
    I.selectOption('#node-input-output', 'json')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()    
})

Scenario('@flow checking - Template', async(I, Flow) => {
    Flow.clickOpen()  
    Flow.clickFlowCreated('Template')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'template - Plain text - Json')
    //I.selectOption('#node-input-syntax', 'plain')
    //I.seeInField('.ace_text-input', '{"payload": "valor: {{payload.data.attrs.teste}}"}')
    I.seeInField('#node-input-output', 'json')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()
})

////////CRON///////
Scenario('@flow Cron - REMOVE', async (Flow, I) => {
    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('Cron')

    Flow.addCron();

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'create')
    I.fillField('#node-input-operation', 'REMOVE')
    I.fillField('#node-input-inJobId', 'jobId')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()    
})

Scenario('@flow checking - Cron - REMOVE', async(I, Flow) => {
    Flow.clickOpen()  
    Flow.clickFlowCreated('Cron')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'create')
    I.seeInField('#node-input-operation', 'REMOVE')
    I.seeInField('#node-input-inJobId', 'jobId')
    Flow.clickOnDone();
    I.wait(1)
    Flow.clickOnSave()
})

////////CRON BATCH///////
Scenario('@flow Cron Batch - REMOVE', async (Flow, I) => {
    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('CronBatch')

    Flow.addCronBatch();

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'cron-batch')
    I.selectOption('#node-input-operation', 'REMOVE')
    I.fillField('#node-input-inJobIds', 'reqJOB')
    I.fillField('#node-input-timeout', '1000')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()    
})

Scenario('@flow checking - Cron Batch - REMOVE', async(I, Flow) => {
    Flow.clickOpen()  
    Flow.clickFlowCreated('CronBatch')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'cron-batch')
    I.seeInField('#node-input-operation', 'REMOVE')
    I.seeInField('#node-input-inJobIds', 'reqJOB')
    I.seeInField('#node-input-timeout', '1000')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()
})

//////DEVICE IN///////
Scenario('@flow DEVICE IN - true', async (Flow, I) => {
    Flow.init(I);

    const deviceId = await Flow.createDevice('Device-test');
    
    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('DEVICE-IN')

    Flow.addDeviceIn()

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'Device-in')
    Flow.selectDeviceTeste(deviceId, 'Device-test')
    I.selectOption('#node-input-status', 'true')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()    
})

Scenario('@flow checking - DEVICE IN - true', async(I, Flow) => {
    Flow.init(I);

    const deviceId = await Flow.createDevice('Device-test');

    Flow.clickOpen()  
    Flow.clickFlowCreated('DEVICE-IN')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'Device-in')
    //Flow.seeDeviceEventFlowList(deviceId, 'Device-test')
    I.seeInField('#node-input-status', 'true')
    Flow.clickOnDone();
    
    I.wait(1)
    Flow.clickOnSave()
})

Scenario('@flow DEVICE IN - false', async (Flow, I) => {
    Flow.init(I);

    const deviceId = await Flow.createDevice('Device-test');
    
    Flow.clickOpen()
    Flow.clickFlowCreated('DEVICE-IN')

    Flow.addDeviceIn()

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'Device-in')
    Flow.selectDeviceTeste(deviceId, 'Device-test')
    I.selectOption('#node-input-status', 'false')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()    
})

Scenario('@flow checking - DEVICE IN - false', async(I, Flow) => {
    Flow.init(I);

    const deviceId = await Flow.createDevice('Device-test');

    Flow.clickOpen()  
    Flow.clickFlowCreated('DEVICE-IN')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'Device-in')
    //Flow.seeDeviceEventFlowList(deviceId, 'Device-test')
    I.seeInField('#node-input-status', 'false')
    Flow.clickOnDone();
    
    I.wait(1)
    Flow.clickOnSave()
})

//////DEVICE OUT///////
Scenario('@flow DEVICE OUT', async (Flow, I) => {
    Flow.init(I);

    const deviceId = await Flow.createDevice('Device-test');
    
    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('DEVICE-OUT')

    Flow.addDeviceOutput()

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'Device-out-configured')
    I.selectOption('#node-input-device_source', 'configured')
    Flow.selectDeviceTeste(deviceId, 'Device-test')
    I.fillField('#node-input-attrs', 'attrs')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()    
})

Scenario('@flow checking - DEVICE-OUT', async(I, Flow) => {
    Flow.init(I);

    const deviceId = await Flow.createDevice('Device-test');

    Flow.clickOpen()  
    Flow.clickFlowCreated('DEVICE-OUT')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'Device-out-configured')
    I.seeInField('#node-input-device_source', 'configured')
    //Flow.selectDeviceTeste(deviceId, 'Device-test')
    I.seeInField('#node-input-attrs', 'attrs')
    Flow.clickOnDone();
    
    I.wait(1)
    Flow.clickOnSave()
})

Scenario('@flow DEVICE OUT ', async (Flow, I) => {
    Flow.init(I);
    
    Flow.clickOpen()  
    Flow.clickFlowCreated('DEVICE-OUT')

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'Device-out-dynamic')
    I.selectOption('#node-input-device_source', 'dynamic')
    I.fillField('#node-input-device_source_msg', 'test')
    I.fillField('#node-input-attrs', 'attrs')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()    
})

Scenario('@flow checking - DEVICE-OUT', async(I, Flow) => {
    Flow.init(I);

    Flow.clickOpen()  
    Flow.clickFlowCreated('DEVICE-OUT')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'Device-out-dynamic')
    I.seeInField('#node-input-device_source', 'dynamic')
    I.fillField('#node-input-device_source_msg', 'test')
    I.seeInField('#node-input-attrs', 'attrs')
    Flow.clickOnDone();
    
    I.wait(1)
    Flow.clickOnSave()
})

//////DEVICE TEMPLATE///////
Scenario('@flow DEVICE TEMPLATE - exclude', async (Flow, I) => {
    Flow.init(I);

    const templateIdFlow = await Flow.createTemplate('Template');
    
    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('DEVICE TEMPLATE')

    Flow.addTemplateInFlow()

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'device template - exclude')
    Flow.selectTemplateDevice(templateIdFlow, 'Template')
    I.selectOption('#node-input-status', 'false')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()    
})

Scenario('@flow checking - DEVICE TEMPLATE - exclude', async(I, Flow) => {
    Flow.init(I);

    const templateIdFlow = await Flow.createTemplate('Template');

    Flow.clickOpen()  
    Flow.clickFlowCreated('DEVICE TEMPLATE')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'device template - exclude')
    //Flow.seeSelectTemplateDevice(templateIdFlow, 'Template')
    I.seeInField('#node-input-status', 'false')
    Flow.clickOnDone();
    
    I.wait(1)
    Flow.clickOnSave()
})

Scenario('@flow DEVICE TEMPLATE - include', async (Flow, I) => {
    Flow.init(I);

    const templateIdFlow = await Flow.createTemplate('Template');
    
    Flow.clickOpen() 
    Flow.clickFlowCreated('DEVICE TEMPLATE')

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'device template - include')
    Flow.selectTemplateDevice(templateIdFlow, 'Template')
    I.selectOption('#node-input-status', 'true')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()    
})

Scenario('@flow checking - DEVICE TEMPLATE - include', async(I, Flow) => {
    Flow.init(I);

    const templateIdFlow = await Flow.createTemplate('Template');

    Flow.clickOpen()  
    Flow.clickFlowCreated('DEVICE TEMPLATE')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'device template - include')
    //Flow.seeSelectTemplateDevice(templateIdFlow, 'Template')
    I.seeInField('#node-input-status', 'true')
    Flow.clickOnDone();
    
    I.wait(1)
    Flow.clickOnSave()
})

/////ACTUATE///////
Scenario('@flow ACTUATE', async (Flow, I) => {
    Flow.init(I);
    
    const deviceId = await Flow.createDevice('Device-test');

    Flow.clickOpen()
    Flow.clickCreateNew()
    Flow.setFlowName('ACTUATE')

    Flow.addActuate()

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'actuate-specific-device')
    I.selectOption('#node-input-device_source', 'configured')
    Flow.selectDeviceTeste(deviceId, 'Device-test')
    I.fillField('#node-input-attrs', 'command')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()    
})

Scenario('@flow checking - ACTUATE', async(I, Flow) => {
    Flow.init(I);

    const templateIdFlow = await Flow.createTemplate('Template');

    Flow.clickOpen()  
    Flow.clickFlowCreated('ACTUATE')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'actuate-specific-device')
    I.seeInField('#node-input-device_source', 'configured')
   // Flow.selectDeviceTeste(deviceId, 'Device-test')
    I.seeInField('#node-input-attrs', 'command')
    Flow.clickOnDone();
    
    I.wait(1)
    Flow.clickOnSave()
})

Scenario('@flow ACTUATE', async (Flow, I) => {
    Flow.init(I);
    
    const deviceId = await Flow.createDevice('Device-test');

    Flow.clickOpen()  
    Flow.clickFlowCreated('ACTUATE')

    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.fillField('#node-input-name', 'actuate-A device defined during the flow')
    I.selectOption('#node-input-device_source', 'dynamic')
    Flow.selectDeviceTeste(deviceId, 'Device-test')
    I.fillField('#node-input-device_source_msg', 'test')
    I.fillField('#node-input-attrs', 'command')
    Flow.clickOnDone();

    I.wait(1)
    Flow.clickOnSave()  
    I.wait(2)
    Flow.seeFlowHasUpdated() 
})

Scenario('@flow checking - ACTUATE', async(I, Flow) => {
    Flow.init(I);

    const templateIdFlow = await Flow.createTemplate('Template');

    Flow.clickOpen()  
    Flow.clickFlowCreated('ACTUATE')
    
    ids = await I.grabAttributeFrom('.nodegroup', 'id');
    I.click(`#${ids}`);
    I.doubleClick(`#${ids}`)

    I.seeInField('#node-input-name', 'actuate-A device defined during the flow')
    I.seeInField('#node-input-device_source', 'dynamic')
   // Flow.selectDeviceTeste(deviceId, 'Device-test')
    I.fillField('#node-input-device_source_msg', 'test')
    I.seeInField('#node-input-attrs', 'command')
    Flow.clickOnDone();
    
    I.wait(1)
    Flow.clickOnSave()
})

//////GET CONTEXT///////
// Scenario('@flow GET CONTEXT - Flow (String)', async (Flow, I) => {
//     Flow.init(I);
    
//     Flow.clickOpen()
//     Flow.clickCreateNew()
//     Flow.setFlowName('GET CONTEXT')

//     Flow.addGetContext();
//     //I.dragSlider('#palette_node_get_context', 600)

//     ids = await I.grabAttributeFrom('.nodegroup', 'id');
//     I.click(`#${ids}`);
//     I.doubleClick(`#${ids}`)

//     I.fillField('#node-input-name', 'get context - flow(String)')
//     I.selectOption('#node-input-contextLayer', 'flow')
//     I.fillField('#node-input-contextName', 'test-get')
//     I.fillField('#node-input-contextContent', 'test')
//     Flow.clickOnDone();

//     I.wait(1)
//     Flow.clickOnSave()    
// })

//REMOVE FLOW
Scenario('@flow REMOVE FLOW', async(I, Flow) => {
    Flow.init(I);
    Flow.clickOpen()

    Flow.clickRemoveFlow('1_FluxoSanity')
    Flow.seeFlowRemoved()
})

Scenario('@flow REMOVE FLOW', async(I, Flow) => {
    Flow.init(I);
    Flow.clickOpen()

    Flow.clickRemoveFlow('2_FluxoSanity')
    Flow.seeFlowRemoved()
})

Scenario('@flow REMOVE FLOW', async(I, Flow) => {
    Flow.init(I);
    Flow.clickOpen()

    Flow.clickRemoveFlow('3_FluxoSanity')
    Flow.seeFlowRemoved()
})