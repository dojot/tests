const Utils = require('../Utils');

Feature('Tenant verification');

newUser = () => ({
    name: 'Random Morty',
    username: `a${Utils.sid()}`,
    service: `a${Utils.sid()}`,
    email: `${Utils.sid()}@noemail.com`,
    profile: 'admin',
});

const jsonTemplate = {
    label: 'String Template',
    attrs: [
        {
            label: 'text',
            type: 'dynamic',
            value_type: 'string',
        },
    ],
};


async function CreateTemplateAndDeviceByJSON(I, templ, dev) {
    const template = await I.createTemplate(templ);
    const templateId = template.template.id;
    const device = await I.createDevice({
        templates: [templateId],
        label: dev,
    });
    I.wait(1);
    return device.devices[0].id;
}

function checkMessage(I, Device, deviceId, msg) {
    I.amOnPage(`#/device/id/${deviceId}/detail`);
    I.wait(2);
    Device.selectAttr('text');
    I.wait(3);
    Device.shouldSeeMessage(msg);
}

function checkingTenant(I, tenant) {
    I.click(locate('div').withAttr({ title: 'Login details' }));
    I.seeElement(locate('.logout-page-info').withText(tenant));
    I.click(locate('div').withAttr({ title: 'Login details' }));
}

function logout(I) {
    I.click(locate('div').withAttr({ title: 'Login details' }));
    I.click('.btn-logout');
    I.wait(3);
}

function genericLogin(I, username, pass = 'temppwd') {
    logout(I);
    I.see('Sign in');
    I.fillField('Username', username);
    I.fillField('Password', pass);
    I.click('Login');
    I.wait(3);
}

/*
    This scenario checks if a new user inherits the parent's tenant. Besides that, checks when an admin changes the user metadata, the tenant still the same.
*/

Scenario('@adv: Checking child tenant equals parent tenant', async (I, Commons, User) => {
    // At first, do login
    I.loginAdmin(I, false);

    // Create a user A using API with a different tenant
    // 1. create User A
    const jUserA = newUser();
    const jUserB = newUser();
    await I.createUser(jUserA);

    // Logout and Login user A
    genericLogin(I, jUserA.username);

    // Create via GUI user B
    User.init(I);
    User.openUserPage();
    User.clickCreateNew();
    User.fillAndSave(jUserB);
    User.seeHasCreated();

    // Logout and Login user B
    genericLogin(I, jUserB.username);

    // Check with user B has the same tenant than user A
    checkingTenant(I, jUserA.service);

    // Login admin
    genericLogin(I, 'admin', 'admin');

    // Edit user B
    User.openUserPage();
    Commons.clickCardByName(jUserB.name);
    User.fillEmailAndSave(`w${Utils.sid()}@noemail.com`);
    User.seeHasUpdated();

    // Logout and Login user B
    genericLogin(I, jUserB.username);

    // Check with user B has the same tenant than user A
    checkingTenant(I, jUserA.service);

    // back to admin
    genericLogin(I, 'admin', 'admin');
    User.openUserPage();

    // remove user A
    Commons.clickCardByName(jUserA.name);
    User.clickRemove();
    User.confirmRemove();
    User.seeHasRemoved();

    // remove user B
    Commons.clickCardByName(jUserB.name);
    User.clickRemove();
    User.confirmRemove();
    User.seeHasRemoved();

    logout(I);
});


Scenario('@adv: Checking message in 2 tenants', async (I, Device) => {
    // At first, do login
    I.loginAdmin(I, false);

    // create variables
    Device.init(I);
    genericLogin(I, 'admin', 'admin');

    const deviceA = 'device A';
    const deviceB = 'device B';
    const userA = newUser();
    const userB = newUser();
    let deviceId = 0;

    // 1. create User A
    await I.createUser(userA);

    // 2. create User B
    await I.createUser(userB);

    // 3 .Login user A
    genericLogin(I, userA.username);

    // 4. create Template and Device for User A
    const templateA = jsonTemplate;
    templateA.label = 'template A';
    deviceId = await CreateTemplateAndDeviceByJSON(I, templateA, deviceA);

    // 5. Checking devices
    Device.clickOpenDevicePage();
    I.refreshPage();
    Device.checkExistCard(deviceA);
    Device.checkNonExistCard(deviceB);

    // 6. Send Message in User A device, to go detail page and check the message
    await I.sendMQTTMessage(deviceId, '{"text": "data A"}', userA.service);
    checkMessage(I, Device, deviceId, 'data A');

    // 7. login User B
    genericLogin(I, userB.username);

    // 8. create Template and Device for User B
    const templateB = jsonTemplate;
    templateB.label = 'template B';
    deviceId = await CreateTemplateAndDeviceByJSON(I, templateB, deviceB);

    // 9. Checking devices
    Device.clickOpenDevicePage();
    I.refreshPage();
    Device.checkExistCard(deviceB);
    Device.checkNonExistCard(deviceA);

    // 10. Send Message in User B device, to go detail page and check the message
    await I.sendMQTTMessage(deviceId, '{"text": "data B"}', userB.service);
    checkMessage(I, Device, deviceId, 'data B');

    logout(I);
});
