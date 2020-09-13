const counterId = document.querySelector('#counter');

const formFieldIngredinet = document.querySelector('.form__field-group-ingredientes');
const nameIngredient = document.querySelector('#nameIngredient');
const formDropdownItems = document.querySelector('.form__dropdown-items');
const cantidadVal = document.querySelector('#cantidadVal');
const cantidad = document.querySelector('#cantidad')
const addIng = document.querySelector('#addIng');
const totalFormIngredients = document.getElementById('id_ingredient_details-TOTAL_FORMS')

const api = new Api(apiUrl);
const header = new Header(counterId);


function Ingredients() {
    let cur = document.querySelectorAll('.form__field-item-ingredient').length;
    // клик по элементам с сервера
    const dropdown = (e) => {
        if (e.target.classList.contains('form__item-list')) {
            nameIngredient.value = e.target.textContent;
            formDropdownItems.style.display = ''
            cantidadVal.textContent = e.target.getAttribute('data-val');
        }
    };
    // Добавление элемента из инпута
    const addIngredient = (e) => {
        if(nameIngredient.value && cantidad.value) {
            const data = getValue();
            const elem = document.createElement('div');
            elem.classList.add('form__field-item-ingredient');
            elem.id = `ing${cur}`;
            elem.innerHTML = `<span> ${data.name} ${data.value}${data.units}</span> <span class="form__field-item-delete"></span>
                             <input id="nameIngredient_${cur}" name="ingredient_details-${cur}-foodstuff" type="hidden" value="">
                             <input id="nameIngredient_${cur}" name="ingredient_details-${cur}-foodstuff_name" type="hidden" value="${data.name}">
                             <input id="valueIngredient_${cur}" name="ingredient_details-${cur}-quantity" type="hidden" value="${data.value}">
                             <input id="unitsIngredient_${cur}" name="ingredient_details-${cur}-dimension" type="hidden" value="${data.units}">`;
            cur++;
            elem.addEventListener('click', eventDelete);
            formFieldIngredinet.insertAdjacentElement('afterend',elem);
            totalFormIngredients.value = cur;
        }
    };
    // удаление элемента
    const eventDelete = (e) => {
        if(e.target.classList.contains('form__field-item-delete')) {
            const item = e.target.closest('.form__field-item-ingredient');
            item.removeEventListener('click',eventDelete);
            item.remove()
        };
    };
    // получение данных из инпутов для добавления
    const getValue = (e) => {
        const data = {
            name: nameIngredient.value,
            value: cantidad.value,
            units: cantidadVal.textContent
        };
        clearValue(nameIngredient);
        clearValue(cantidad);
        return data;
    };
    // очистка инпута
    const clearValue = (input) => {
        input.value = '';
    };
    return {
        clearValue,
        getValue,
        addIngredient,
        dropdown
    }
}

const cbEventInput = (elem) => {
    return api.getIngredients(elem.target.value).then( e => {
        if(e.length !== 0 ) {
            const items = e.map( elem => {
                return `<a class="form__item-list" data-val="${elem.dimension}"">${elem.name}</a>`
            }).join(' ')
            formDropdownItems.style.display = 'flex';
            formDropdownItems.innerHTML = items;
        }
    })
    .catch( e => {
        console.log(e)
    })
};

const eventInput = debouncing(cbEventInput, 1000);

// вешаем апи
nameIngredient.addEventListener('input', eventInput);
const ingredients = Ingredients();
// вешаем слушатель на элементы с апи
formDropdownItems.addEventListener('click', ingredients.dropdown);
// вешаем слушатель на кнопку
addIng.addEventListener('click', ingredients.addIngredient);


const eventDelete = (e) => {
    if(e.target.classList.contains('form__field-item-delete')) {
        const item = e.target.closest('.form__field-item-ingredient');
        item.removeEventListener('click',eventDelete);
        item.remove()
    };
};
const ingredientItemElements = document.querySelectorAll('.form__field-item-ingredient')
for (let elem of ingredientItemElements) {
    elem.addEventListener('click', eventDelete);
}
