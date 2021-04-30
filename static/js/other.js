var loginNumber = 1;
function addField() {
	var form = document.getElementById('form');
	var button = document.getElementById('button');
	var newFillingForm = document.createElement('p');
	newFillingForm.innerHTML = `<label>Добавить участника: </label><input type="text" maxlength="20" name="login${loginNumber}" value=""/>`;
	loginNumber += 1;
	form.insertBefore(newFillingForm, button);
}