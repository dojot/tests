let I = actor();
const Util = require('../Utils');

module.exports = {
    FieldsLabel: {},

    ButtonLabel: {
        add: 'Add',
        remove: 'Remove',
        save: 'Save',
        discard: 'Discard',
    },

    ClassesCSS: {},

    AttributeType: {
        dynamic: 'Dynamic Value',
        static: 'Static Value',
        actuator: 'Actuator',
    },

    AttributeValueType: {
        boolean: 'Boolean',
        geo: 'Geo',
        float: 'Float',
        integer: 'Integer',
        string: 'String',
    },

    ConfigurationType: {
        protocol: 'Protocol',
    },

    init(i) {
        I = i;
    },

    convertToObjectMeta(labelValue, typeValue, attrValueType, value) {
        return this.convertToObjectMetaToAdd(labelValue, typeValue, attrValueType, value);
    },

    convertToObjectMetaToAdd(labelValue, typeValue, attrValueType, value) {
        return {
            labelValue,
            typeValue,
            attrValueType,
            value,
        };
    },

    convertToObjectMetaToUpdate(oldLabelValue, newLabelValue, newTypeValue, newAttrValueType, newValue) {
        return { oldLabelValue, ...this.convertToObjectMetaToAdd(newLabelValue, newTypeValue, newAttrValueType, newValue) };
    },

    convertToObjectMetaToRemove(removeLabelValue) {
        return { removeLabelValue };
    },

    clickOpenTemplatePage() {
        I.waitForElement(locate('a').withAttr({ href: '#/template/list' }));
        I.click(locate('a').withAttr({ href: '#/template/list' }));
    },

    fillNameTemplate(value) {
        I.fillField('Template Name', value);
    },

    change64QtyToShowPagination() {
        I.selectOption(locate('select').inside('.card-select-2'), '64');
    },

    seeNameTemplate(value) {
        I.seeInputByNameAndValue('Template Name', value);
    },

    clickCreateNew() {
        I.waitForElement(locate('div').withAttr({ title: 'Create a new template' }));
        I.click(locate('div').withAttr({ title: 'Create a new template' }));
    },

    clickCardByNameTemplate(nameTemplate) {
        I.waitForElement(locate('div').withAttr({ title: nameTemplate }));
        I.click(locate('div').withAttr({ title: nameTemplate }));
    },

    _fillAttrForm(fieldValue, attrType, attrValueType, value) {
        within('.sidebar-attribute', () => {
            I.fillField(locate('input').first(), fieldValue);
            I.fillSelectByName('type', attrType);
            I.fillSelectByName('value_type', attrValueType);
            if ((attrType !== this.AttributeType.dynamic || attrType !== this.AttributeType.actuator) && value) {
                I.fillField(locate('input').withAttr({ name: 'static_value' }), Util.toString(value));
            }
        });
    },

    _fillMetaForm(labelValue, typeValue, attrValueType, value) {
        within('.sidebar-metadata', () => {
            I.fillField('label', labelValue);
            I.fillField('type', typeValue);
            I.fillSelectByName('value_type', attrValueType);
            I.fillField('static_value', Util.toString(value));
        });
    },

    _addMeta(labelValue, typeValue, attrValueType, value) {
        this._clickOpenFooterBtnNew('New Metadata');
        this._fillMetaForm(labelValue, typeValue, attrValueType, value);
        I.click(this.ButtonLabel.add);
    },

    _updateMeta(oldLabelValue, newLabelValue, newTypeValue, newAttrValueType, newValue) {
        this._clickToEditAMeta(oldLabelValue);
        this._fillMetaForm(newLabelValue, newTypeValue, newAttrValueType, newValue);
        I.click(this.ButtonLabel.save);
    },

    addAttr(fieldValue, attrType, attrValueType, metaDataArray, value = '') {
        this._clickOpenFooterBtnNew('New Attribute');
        this._fillAttrForm(fieldValue, attrType, attrValueType, value);
        this._metasArrayToAddUpdateRemove(metaDataArray);
        within('.sidebar-attribute', () => {
            I.click(this.ButtonLabel.add);
        });
    },

    _metasArrayToAddUpdateRemove(metaDataArray) {
        metaDataArray.forEach((meta) => {
            if (meta.oldLabelValue) {
                this._updateMeta(meta.oldLabelValue, meta.labelValue, meta.typeValue, meta.attrValueType, meta.value);
            } else if (meta.removeLabelValue) {
                this._removeMeta(meta.removeLabelValue);
            } else {
                this._addMeta(meta.labelValue, meta.typeValue, meta.attrValueType, meta.value);
            }
        });
    },

    updateAttr(oldFieldValue, newFieldValue, newAttrType, newAttrValueType, metaDataArray, newValue = '') {
        this._clickToEditAAttr(oldFieldValue);
        this._fillAttrForm(newFieldValue, newAttrType, newAttrValueType, newValue);
        this._metasArrayToAddUpdateRemove(metaDataArray);
        within('.sidebar-attribute', () => {
            I.click(this.ButtonLabel.save);
        });
    },

    seeAttrHasRemoved(oldFieldValue) {
        I.dontSeeElement(locate('.template-prop').withAttr({ title: oldFieldValue, role: 'button' }));
    },

    _clickToEditAMeta(labelValue) {
        I.waitForElement(locate('.metadata-label').withText(labelValue).inside('.metadata-list-item'));
        I.click(locate('.metadata-label').withText(labelValue).inside('.metadata-list-item'));
    },

    _seeMeta(labelValue, typeValue, attrValueType, value) {
        this._clickToEditAMeta(labelValue);
        within('.sidebar-metadata', () => {
            I.seeInputByNameAndValue('label', labelValue);
            I.seeInputByNameAndValue('type', typeValue);
            I.seeSelectOptionByNameAndValue('value_type', attrValueType);
            I.seeInputByNameAndValue('static_value', Util.toString(value));
            I.click(this.ButtonLabel.discard);
        });
    },

    seeAttr(fieldValue, attrType, attrValueType, metaDataArray, value = null) {
        this._clickToEditAAttr(fieldValue);
        within('.sidebar-attribute', () => {
            I.seeInputByNameAndValue('label', fieldValue);
            if (value) {
                I.seeInputByNameAndValue('static_value', Util.toString(value));
            }
            I.seeSelectOptionByNameAndValue('type', attrType);
            I.seeSelectOptionByNameAndValue('value_type', attrValueType);
            if ((attrType !== this.AttributeType.dynamic || attrType !== this.AttributeType.actuator) && value) {
                I.seeInputByNameAndValue('static_value', Util.toString(value));
            }
        });
        metaDataArray.forEach((meta) => {
            this._seeMeta(meta.labelValue, meta.typeValue, meta.attrValueType, meta.value);
        });
        within('.sidebar-attribute', () => {
            I.click(this.ButtonLabel.discard);
        });
    },

    _removeMeta(labelValue) {
        this._clickToEditAMeta(labelValue);
        within('.sidebar-metadata', () => {
            I.seeInputByNameAndValue('label', labelValue);
            I.click(this.ButtonLabel.remove);
        });

        I.click('Confirm');
    },

    _clickToEditAAttr(label) {
        I.waitForElement(locate('.template-prop').withAttr({ title: label, role: 'button' }));
        I.click(locate('.template-prop').withAttr({ title: label, role: 'button' }));
    },

    removeAttr(fieldValue, metaDataArray) {
        this._clickToEditAAttr(fieldValue);
        within('.sidebar-attribute', () => {
            I.seeInputByNameAndValue('label', fieldValue);
        });
        this._metasArrayToAddUpdateRemove(metaDataArray);
        within('.sidebar-attribute', () => {
            I.click(this.ButtonLabel.remove);
        });
        I.click('Confirm');
    },

    _fillConfigForm(confType, value) {
        within('.sidebar-attribute', () => {
            I.fillSelectByName('label', confType);
            I.fillField('static_value', value);
        });
    },

    addConfigTemplate(confType, value) {
        this._clickOpenFooterBtnNew('New Configuration');
        this._fillConfigForm(confType, value);
        I.click(this.ButtonLabel.add);
    },

    seeConfigTemplate(confType, value) {
        this._clickToEditAAttr(confType.toLowerCase());
        within('.sidebar-attribute', () => {
            I.seeSelectOptionByNameAndValue('label', confType);
            I.seeInputByNameAndValue('static_value', Util.toString(value));
            I.click(this.ButtonLabel.discard);
        });
    },

    updateConfigTemplate(oldConfType, newConfType, value) {
        this._clickToEditAAttr(oldConfType.toLowerCase());
        this._fillConfigForm(newConfType, value);
        I.click(this.ButtonLabel.save);
    },

    removeConfigTemplate(confType) {
        this._clickToEditAAttr(confType.toLowerCase());
        within('.sidebar-attribute', () => {
            I.seeSelectOptionByNameAndValue('label', confType);
            I.click(this.ButtonLabel.remove);
        });
        I.click('Confirm');
        I.wait(1);
    },

    _clickOpenFooterBtnNew(labelBtn) {
        I.waitForElement(locate('.body-actions--button div').withText(labelBtn));
        I.click(locate('.body-actions--button div').withText(labelBtn));
    },

    seeManageFirmware() {
        this._clickOpenFooterBtnNew('Manage Firmware');
        I.waitForElement(locate('.firmware-enabled'), 5);
        I.click(locate('.firmware-enabled'));
        I.click(this.ButtonLabel.discard);
        I.wait(1);
    },

    clickSave() {
        I.click(this.ButtonLabel.save);
    },

    clickDiscard() {
        I.click(this.ButtonLabel.discard);
        I.wait(1);
    },

    seeTemplateHasCreated() {
        I.wait(3);
        I.see('Template created.');
    },

    removeTemplate() {
        I.click(this.ButtonLabel.remove);
        I.click('Confirm');
        I.wait(1);
    },

    seeTemplateHasDelete() {
        I.wait(3);
        I.see('Template removed.');
    },

    seeTemplateHasUpdated() {
        I.wait(3);
        I.see('Template updated.');
    },
};
