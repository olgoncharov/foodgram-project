const container_subscribe = document.querySelector('.author-subscribe');
const configButton2 = {
    subscribe: {
        attr: 'data-out',
        default: {
            class: 'button_style_blue',
            text: 'Подписаться на автора'
        },
        active: {
            class: 'button_style_blue',
            text: `Отписаться от автора`
        }
    }
}
const subscribe = new Subscribe(configButton2.subscribe, api);

const authorRecipeSubscribe = new AuthorRecipe(container_subscribe, '.author-subscribe', header, api, true, {
    subscribe
});

authorRecipeSubscribe.addEvent();