Feature('Template CRUD');

Before((login) => {
    login('admin');
});

Scenario('@basic: Creating a template', async (I, Template) => {
    Template.init(I);
    Template.clickOpenTemplatePage();
    Template.clickCreateNew();
    Template.fillNameTemplate('1_NameOfTemplate');

    /*    Template.addConfigTemplate(
            Template.ConfigurationType.protocol,
            'mqtt',
        );

        Template.updateConfigTemplate(
            Template.ConfigurationType.protocol,
            Template.ConfigurationType.protocol,
            'mqtt2',
        ); */

    Template.addAttr(
        'attrStringStatic',
        Template.AttributeType.static,
        Template.AttributeValueType.string,
        [
            Template.convertToObjectMetaToAdd(
                'metaString',
                'typeValueMetaString',
                Template.AttributeValueType.string,
                'valueMetaString',
            ),
            Template.convertToObjectMetaToAdd(
                'metaBool',
                'typeValueMetaBool',
                Template.AttributeValueType.boolean,
                false,
            ),
        ],
        'Value of text',
    );

    Template.addAttr(
        'attrIntegerDynamic',
        Template.AttributeType.dynamic,
        Template.AttributeValueType.integer,
        [
            Template.convertToObjectMetaToAdd(
                'metaString',
                'typeValueMetaString',
                Template.AttributeValueType.string,
                'valueMetaString',
            ),
            Template.convertToObjectMetaToAdd(
                'metaBool',
                'typeValueMetaBool',
                Template.AttributeValueType.boolean,
                false,
            ),
            Template.convertToObjectMetaToRemove(
                'metaString',
            ),
            Template.convertToObjectMetaToUpdate(
                'metaBool',
                'metaChangeFromBoolToFloat',
                'typeValueMetaFloat',
                Template.AttributeValueType.float,
                3.14,
            ),
        ],
    );

    Template.addAttr(
        'attrGPSStatic',
        Template.AttributeType.static,
        Template.AttributeValueType.geo,
        [
            Template.convertToObjectMetaToAdd(
                'metaString',
                'typeValueMetaString',
                Template.AttributeValueType.string,
                'valueMetaString',
            ),
        ],
        '-22.826702502573774, -47.044628078647314',
    );

    /*    Template.addAttr(
        'attrStringActuator',
        Template.AttributeType.actuator,
        Template.AttributeValueType.string,
    ); */

    Template.updateAttr(
        'attrGPSStatic',
        'attrGPSStaticChange',
        Template.AttributeType.static,
        Template.AttributeValueType.geo,
        [],
        '-23.826702502573774, -48.044628078647314',
    );

    Template.clickSave();
    Template.seeTemplateHasCreated();
});

Scenario('@basic: Checking create template', async (I, Template) => {
    Template.init(I);
    Template.clickOpenTemplatePage();
    Template.change64QtyToShowPagination();
    Template.clickCardByNameTemplate('1_NameOfTemplate');
    Template.seeNameTemplate('1_NameOfTemplate');

    /*    Template.seeConfigTemplate(
            Template.ConfigurationType.protocol,
            'mqtt2',
        ); */

    Template.seeAttr(
        'attrStringStatic',
        Template.AttributeType.static,
        Template.AttributeValueType.string,
        [
            Template.convertToObjectMeta(
                'metaString',
                'typeValueMetaString',
                Template.AttributeValueType.string,
                'valueMetaString',
            ),
            Template.convertToObjectMeta(
                'metaBool',
                'typeValueMetaBool',
                Template.AttributeValueType.boolean,
                false,
            ),
        ],
        'Value of text',
    );

    Template.seeAttr(
        'attrIntegerDynamic',
        Template.AttributeType.dynamic,
        Template.AttributeValueType.integer,
        [
            Template.convertToObjectMeta(
                'metaChangeFromBoolToFloat',
                'typeValueMetaFloat',
                Template.AttributeValueType.float,
                3.14,
            ),
        ],
    );


    Template.seeAttr(
        'attrGPSStaticChange',
        Template.AttributeType.static,
        Template.AttributeValueType.geo,
        [
            Template.convertToObjectMeta(
                'metaString',
                'typeValueMetaString',
                Template.AttributeValueType.string,
                'valueMetaString',
            ),
        ],
        '-23.826702502573774, -48.044628078647314',
    );

    /*    Template.seeAttr(
        'attrStringActuator',
        Template.AttributeType.actuator,
        Template.AttributeValueType.string,
    ); */

    Template.seeManageFirmware();
    Template.clickDiscard();
});

Scenario('@basic: Updating a template', async (I, Template) => {
    Template.init(I);
    Template.clickOpenTemplatePage();
    Template.change64QtyToShowPagination();
    Template.clickCardByNameTemplate('1_NameOfTemplate');
    Template.seeNameTemplate('1_NameOfTemplate');
    Template.fillNameTemplate('2_NameOfTemplate');
    Template.updateAttr(
        'attrIntegerDynamic',
        'attrIntegerDynamicChange',
        Template.AttributeType.static,
        Template.AttributeValueType.integer,
        [
            Template.convertToObjectMetaToUpdate(
                'metaChangeFromBoolToFloat',
                'metaBoolChange',
                'typeValueMetaBool',
                Template.AttributeValueType.boolean,
                true,
            ),
        ],
        10,
    );

    /*    Template.updateConfigTemplate(
            Template.ConfigurationType.protocol,
            Template.ConfigurationType.topic,
            'topic',
        ); */
    /*    Template.addConfigTemplate(
            Template.ConfigurationType.protocol,
            'mqtt',
        ); */

    Template.addAttr(
        'attrBoolStatic',
        Template.AttributeType.static,
        Template.AttributeValueType.integer,
        [
            Template.convertToObjectMetaToAdd(
                'metaString2',
                'typeValueMetaString2',
                Template.AttributeValueType.string,
                'valueMetaString2',
            ),
            Template.convertToObjectMetaToAdd(
                'metaBool2',
                'typeValueMetaBool2',
                Template.AttributeValueType.boolean,
                false,
            ),
            Template.convertToObjectMetaToRemove(
                'metaString2',
            ),
            Template.convertToObjectMetaToUpdate(
                'metaBool2',
                'metaChangeFromBoolToFloat2',
                'typeValueMetaFloat2',
                Template.AttributeValueType.float,
                3.14,
            ),
        ],
        45,
    );


    Template.removeAttr(
        'attrStringStatic',
        [
            Template.convertToObjectMetaToRemove(
                'metaString',
            ),
        ],
    );

    Template.seeManageFirmware();
    Template.clickSave();
    Template.seeTemplateHasUpdated();
});

Scenario('@basic: Checking update template', async (I, Template) => {
    Template.init(I);
    Template.clickOpenTemplatePage();
    Template.change64QtyToShowPagination();
    Template.clickCardByNameTemplate('2_NameOfTemplate');
    Template.seeNameTemplate('2_NameOfTemplate');
    Template.seeAttr(
        'attrIntegerDynamicChange',
        Template.AttributeType.static,
        Template.AttributeValueType.integer,
        [
            Template.convertToObjectMeta(
                'metaBoolChange',
                'typeValueMetaBool',
                Template.AttributeValueType.boolean,
                true,
            ),
        ],
        10,
    );

    /*    Template.seeConfigTemplate(
            Template.ConfigurationType.topic,
            'topic',
        ); */

    /*    Template.seeConfigTemplate(
            Template.ConfigurationType.protocol,
            'mqtt',
        ); */

    Template.seeAttr(
        'attrBoolStatic',
        Template.AttributeType.static,
        Template.AttributeValueType.boolean,
        [
            Template.convertToObjectMeta(
                'metaChangeFromBoolToFloat2',
                'typeValueMetaFloat2',
                Template.AttributeValueType.float,
                3.14,
            ),
        ],
        false,
    );
    Template.seeAttrHasRemoved('attrStringStatic');
    Template.seeManageFirmware();
    Template.clickDiscard();
});

Scenario('@basic: Removing template', async (I, Template) => {
    Template.init(I);
    Template.clickOpenTemplatePage();
    Template.change64QtyToShowPagination();
    Template.clickCardByNameTemplate('2_NameOfTemplate');
    Template.seeNameTemplate('2_NameOfTemplate');
    Template.removeAttr('attrIntegerDynamicChange', [
        Template.convertToObjectMetaToRemove('metaBoolChange'),
    ]);

    /*  Template.removeConfigTemplate(Template.ConfigurationType.topic); */

    Template.seeAttrHasRemoved('attrIntegerDynamicChange');

    Template.removeTemplate();
    Template.seeTemplateHasDelete();
});
