// TESTE DEVICE
Feature('Device CRUD');

Before((login) => {
    login('admin');
});

const template1 = {
    id: null,
    name: '1 - Template',
    attrsDynamics: [
        {
            value_type: 'boolean',
            label: 'bool',
            type: 'dynamic',
        },
        {
            value_type: 'float',
            label: 'float',
            type: 'dynamic',
            metadata: [
                {
                    label: 'unit',
                    static_value: 'empty',
                    type: 'temperature',
                    value_type: 'string',
                },
            ],
        },
        {
            value_type: 'geo:point',
            label: 'gps',
            type: 'dynamic',
        },
        {
            value_type: 'integer',
            label: 'int',
            type: 'dynamic',
        },
        {
            value_type: 'string',
            label: 'str',
            type: 'dynamic',
        }],
    attrsStatics: [
        {
            value_type: 'string',
            label: 'serial',
            type: 'static',
            static_value: 'undefined',
            metadata: [
                {
                    label: 'meta1',
                    static_value: 10,
                    type: 'type_meta',
                    value_type: 'integer',
                },
                {
                    label: 'meta2',
                    static_value: 'value',
                    type: 'type_string_x',
                    value_type: 'string',
                },
                {
                    label: 'meta3',
                    static_value: 'value',
                    type: 'type_string_x',
                    value_type: 'string',
                },
            ],
        },
        {
            value_type: 'string',
            label: 'str_static',
            type: 'static',
            static_value: 'undefined',
        },
        {
            value_type: 'string',
            label: 'str_static2',
            type: 'static',
            static_value: 'undefined',
        },
    ],
    attrsConfig: [
        {
            value_type: 'string',
            label: 'protocol',
            type: 'meta',
            static_value: 'mqtt',
        },
    ],
    attrsActuators: [
        {
            value_type: 'string',
            label: 'msg',
            type: 'actuator',
            static_value: '',
        },
    ],
    json: {},
};
const loadJson = (template) => {
    template.json = {
        label: template.name,
        attrs: [
            ...template.attrsActuators,
            ...template.attrsConfig,
            ...template.attrsStatics,
            ...template.attrsDynamics,
        ],
    };
};

loadJson(template1);

function checkingAttrTemplate(Device, template) {
/*    Device.clickToManageAttributes(Device.AttributeTypes.configuration);
    Device.seeAllConfigurations(template.attrsConfig);
    Device.clickDiscard(); */

    Device.clickToManageAttributes(Device.AttributeTypes.dynamic);
    Device.seeAllDynamics(template.attrsDynamics);
    Device.clickDiscard();

    Device.clickToManageAttributes(Device.AttributeTypes.static);
    Device.seeAllStatic(template.attrsStatics);
    Device.clickDiscard();


    Device.clickToManageAttributes(Device.AttributeTypes.actuator);
    Device.seeAllDynamics(template.attrsActuators);
    Device.clickDiscard();
}

Scenario('@basic: Creating a device', async (I, Device) => {
    const template = await I.createTemplate(template1.json);
    template1.id = template.template.id;

    Device.init(I);
    Device.clickOpenDevicePage();
    Device.change64QtyToShowPagination();

    I.refreshPage();

    Device.clickCreateNew();
    Device.fillNameDevice('Name of device');
    Device.clickAddOrRemoveTemplate();
    Device.clickToSelectTemplate(template1.name);
    Device.clickBack();

    checkingAttrTemplate(Device, template1);

    Device.fillAttrStaticValue('serial', 'ABCDEFG-86');
    Device.fillAttrStaticValue('str_static2', 'ABC2');
    /* Device.fillConfigurationValue(Device.ConfigurationType.protocol, 'mqtt2'); */
    Device.fillMetaStaticValue('serial', 'meta1', 22);
    Device.fillMetaStaticValue('serial', 'meta3', 'value2');
    Device.fillMetaDynamicValue('float', 'unit', '40');

    Device.clickSave();

    Device.seeHasCreated();
});

Scenario('@basic: Checking a device create', async (I, Device) => {
    Device.init(I);
    Device.change64QtyToShowPagination();
    Device.clickCardByDeviceName('Name of device');

    const templateJustToCheck = JSON.parse(JSON.stringify(template1));
    templateJustToCheck.attrsStatics[0].static_value = 'ABCDEFG-86';
    templateJustToCheck.attrsConfig[0].static_value = 'mqtt2';
    templateJustToCheck.attrsStatics[0].metadata[0].static_value = 22;
    templateJustToCheck.attrsStatics[0].metadata[2].static_value = 'value2';
    templateJustToCheck.attrsStatics[2].static_value = 'ABC2';
    templateJustToCheck.attrsDynamics[1].metadata[0].static_value = '40';
    checkingAttrTemplate(Device, templateJustToCheck);

    Device.clickDiscard();
});

Scenario('@basic: Updating a device', async (I, Device) => {
    Device.init(I);
    Device.change64QtyToShowPagination();
    Device.clickCardByDeviceName('Name of device');
    Device.fillNameDevice('Name of device change');

    Device.fillAttrStaticValue('serial', 'change-ABCDEFG-86');
    /* Device.fillConfigurationValue(Device.ConfigurationType.protocol, 'mqtt3'); */
    Device.fillMetaStaticValue('serial', 'meta1', 10);
    Device.fillMetaDynamicValue('float', 'unit', '11');
    Device.fillAttrStaticValue('str_static2', 'ABC');

    Device.clickSave();

    Device.seeHasUpdated();
});

Scenario('@basic: Checking a device update', async (I, Device) => {
    Device.init(I);
    Device.change64QtyToShowPagination();
    Device.clickCardByDeviceName('Name of device change');

    const templateJustToCheck = JSON.parse(JSON.stringify(template1));
    templateJustToCheck.attrsStatics[0].static_value = 'change-ABCDEFG-86';
    templateJustToCheck.attrsConfig[0].static_value = 'mqtt3';
    templateJustToCheck.attrsStatics[0].metadata[0].static_value = 10;
    templateJustToCheck.attrsDynamics[1].metadata[0].static_value = '11';
    templateJustToCheck.attrsStatics[0].metadata[2].static_value = 'value2';
    templateJustToCheck.attrsStatics[2].static_value = 'ABC';
    checkingAttrTemplate(Device, templateJustToCheck);

    Device.clickDiscard();
});


Scenario('@basic: Checking after change template', async (I, Device) => {
    // attr serial
    template1.attrsStatics[0].static_value = 'updateValueWithEditOnDevice';
    // meta2
    template1.attrsStatics[0].metadata[1].static_value = 'updateValueWithoutEditOnDevice';
    // meta3
    template1.attrsStatics[0].metadata[2].static_value = 'updateValueWithEditOnDevice';
    // str_static
    template1.attrsStatics[1].static_value = 'updateValueWithoutEditOnDevice';


    await I.updateTemplate(template1.json, template1.id);

    const templateJustToCheck = JSON.parse(JSON.stringify(template1));
    templateJustToCheck.attrsStatics[0].static_value = 'change-ABCDEFG-86';
    templateJustToCheck.attrsConfig[0].static_value = 'mqtt3';
    templateJustToCheck.attrsStatics[0].metadata[0].static_value = 10;
    templateJustToCheck.attrsDynamics[1].metadata[0].static_value = '11';
    templateJustToCheck.attrsStatics[0].metadata[2].static_value = 'value2';
    templateJustToCheck.attrsStatics[2].static_value = 'ABC';

    Device.init(I);
    Device.change64QtyToShowPagination();
    Device.clickCardByDeviceName('Name of device change');

    checkingAttrTemplate(Device, templateJustToCheck);

    Device.clickDiscard();
});

Scenario('@basic: Updating a device - specialized', async (I, Device) => {
    template1.attrsStatics[0].metadata[2].static_value = 'value2';
    template1.attrsStatics[2].static_value = 'ABC';
    template1.attrsConfig[0].static_value = 'mqtt3';

    await I.updateTemplate(template1.json, template1.id);

    Device.init(I);
    Device.change64QtyToShowPagination();
    Device.clickCardByDeviceName('Name of device change');
    Device.fillNameDevice('Name of device');
    Device.clickSave();
    Device.seeHasUpdated();
});


Scenario('@basic: Checking a after specialized change  ', async (I, Device) => {
    template1.attrsConfig[0].static_value = 'mqtt';
    await I.updateTemplate(template1.json, template1.id);

    const templateJustToCheck = JSON.parse(JSON.stringify(template1));
    templateJustToCheck.attrsStatics[0].static_value = 'change-ABCDEFG-86';
    templateJustToCheck.attrsConfig[0].static_value = 'mqtt3';
    templateJustToCheck.attrsStatics[0].metadata[0].static_value = 10;
    templateJustToCheck.attrsDynamics[1].metadata[0].static_value = '11';
    templateJustToCheck.attrsStatics[0].metadata[2].static_value = 'value2';
    templateJustToCheck.attrsStatics[2].static_value = 'ABC';

    Device.init(I);
    Device.change64QtyToShowPagination();
    Device.clickCardByDeviceName('Name of device');


    checkingAttrTemplate(Device, templateJustToCheck);

    Device.clickDiscard();
});


Scenario('@basic: Removing a device', async (I, Device) => {
    Device.init(I);
    Device.change64QtyToShowPagination();
    Device.clickCardByDeviceName('Name of device');
    Device.clickRemove();
    Device.clickConfirm();
    Device.seeHasRemoved();
});
