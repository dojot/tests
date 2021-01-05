Feature('Profiles CRUD');

Before((login) => {
    login('admin');
});

function openPage(I) {
    I.click(locate('a').withAttr({ href: '#/groups' }));
}

Scenario('@basic: Creating a profile', (I) => {
    openPage(I);

    I.wait(10);

    I.click(locate('div').withAttr({ title: 'Create a new profile' }));
    I.fillField('name', 'TesteProfile');
    I.wait(1);
    I.fillField('description', 'Teste Profile, contendo teste automatizado usando codecept - JavaScript');
    I.retry(5).checkOption('template.viewer');
    I.retry(5).checkOption('device.viewer');
    I.retry(5).checkOption('flows.viewer');
    I.retry(5).checkOption('history.viewer');
    I.retry(5).checkOption('user.viewer');
    I.retry(5).checkOption('ca.viewer');
    I.retry(5).checkOption('user.modifier');
    I.retry(5).checkOption('permission.modifier');
    I.retry(5).click('Save');

    // Checking message the reply
    I.wait(2);
    I.retry(5).see('Profile created.');
});

Scenario('@basic: Checking create profile', (I) => {
    openPage(I);
    I.click('TesteProfile');
    I.retry(5).seeCheckboxIsChecked('template.viewer');
    I.retry(5).seeCheckboxIsChecked('device.viewer');
    I.retry(5).seeCheckboxIsChecked('flows.viewer');
    I.retry(5).seeCheckboxIsChecked('history.viewer');
    I.retry(5).seeCheckboxIsChecked('user.viewer');
    I.retry(5).seeCheckboxIsChecked('ca.viewer');
    I.retry(5).seeCheckboxIsChecked('user.modifier');
    I.retry(5).seeCheckboxIsChecked('permission.modifier');
});

Scenario('@basic: Updating a profile', (I) => {
    openPage(I);

    I.click('TesteProfile');
    I.retry(5).uncheckOption('user.viewer');
    I.retry(5).uncheckOption('ca.viewer');
    // I.retry(5).uncheckOption('permission.modifier');
    I.wait(1);

    I.click('Save');
    // Checking message the reply
    I.wait(3);
    I.retry(5).see('Profile updated.');
});

Scenario('@basic: Checking Update profile', (I) => {
    openPage(I);

    I.click('TesteProfile');
    I.retry(5).dontSeeCheckboxIsChecked('user.viewer');
    I.retry(5).dontSeeCheckboxIsChecked('ca.viewer');
    I.retry(5).dontSeeCheckboxIsChecked('permission.modifier');
    I.wait(1);
});

Scenario('@basic: Invalid characters', (I) => {
    openPage(I);

    I.click('TesteProfile');
    I.fillField('name', '--');
    I.fillField('description', 'Teste de Caracteres');
    I.click('Save');

    // Checking message the reply
    I.wait(3);
    I.retry(5).see('Invalid group name, only alphanumeric allowed');
    I.click(locate('.footer button').withAttr({ title: 'Discard' }));
});

Scenario('@basic: Testing discard button', (I) => {
    openPage(I);

    I.click('TesteProfile');
    I.click(locate('.footer button').withAttr({ title: 'Discard' }));
});

Scenario('@basic: Remove profile, Button Cancel', (I) => {
    openPage(I);

    I.click('TesteProfile');
    I.click(locate('.footer button').withAttr({ title: 'Remove' }));
    I.click(locate('.confirm-modal button').withAttr({ title: 'Cancel' }));
    I.wait(2);
});

Scenario('@basic: Remove profile', (I) => {
    openPage(I);

    I.click('TesteProfile');
    I.click(locate('.footer button').withAttr({ title: 'Remove' }));
    I.click(locate('.confirm-modal button').withAttr({ title: 'Remove' }));

    // Checking message the reply
    I.wait(3);
    I.retry(5).see('Profile removed');
});


Scenario('@basic: Creating a profile, description empty', (I) => {
    openPage(I);

    I.click(locate('div').withAttr({ title: 'Create a new profile' }));
    I.fillField('name', 'TesteDescricao');
    I.fillField('description', '');
    I.click('Save');

    I.wait(3);
    I.retry(5).see('Empty Profile description.');
    I.click(locate('.footer button').withAttr({ title: 'Discard' }));
});

Scenario('@basic: Creating a profile, Name empty', (I) => {
    openPage(I);

    I.click(locate('div').withAttr({ title: 'Create a new profile' }));
    I.fillField('name', '');
    I.fillField('description', '');
    I.click('Save');

    I.wait(3);
    I.retry(5).see('Empty Profile name.');
    I.click(locate('.footer button').withAttr({ title: 'Discard' }));
});

// ///////////////////////////////////////////////////////////
//  Teste de usuario e perfil, configurando permissições //
// //////////////////////////////////////////////////////////


// Feature('User Management');

// // Usar outro comando, comando não pratico caso mude o endereço IP
// Scenario('@basic: Open page User', async (I) => {
//     I.amOnPage('#/auth');
// });

// Scenario('@basic: Create a new user', async (I) => {
//     I.click(locate('input').withAttr({ title: 'userName46465' }));
//     I.fillField('userName46465', 'TestUser1');
// });
