const tg = window.Telegram.WebApp;

const STACK_KEY = "navigationStack";
const MAX_STACK_SIZE = 10;

const getNavigationStack = () => {
    const storedStack = sessionStorage.getItem(STACK_KEY);
    console.log(storedStack);
    return storedStack ? JSON.parse(storedStack) : [];
}

const saveNavigationStack = (stack) => {
    sessionStorage.setItem(STACK_KEY, JSON.stringify(stack));
}

const pushToStack = (url) => {
    const stack = getNavigationStack();
    if ((stack.length === 0 || stack[stack.length - 1] !== url) && url !== "/auth") {
        stack.push(url);
        if (stack.length > MAX_STACK_SIZE) {
            stack.shift();
        }
        saveNavigationStack(stack);
    }
}

const handleBackButton = () => {
    const stack = getNavigationStack();
    if (stack.length > 1) {
        stack.pop();
        saveNavigationStack(stack);

        const previousPage = stack[stack.length - 1];
        window.location.href = previousPage;
    } else {
        console.log("Больше нет страниц для возврата.");
        tg.BackButton.hide();
    }
}

pushToStack(window.location.pathname);

const stack = getNavigationStack();
if (stack.length > 1) {
    tg.BackButton.show();
    tg.BackButton.onClick(handleBackButton);
} else {
    tg.BackButton.hide();
}

$(document).ready(() => {
    if (tg.initData) {
        if (!$.cookie('token') && window.location.pathname !== "/auth") {
            const currentPath = window.location.pathname + window.location.search;
            const redirectUrl = `/auth?redirect=${encodeURIComponent(currentPath)}`;
            window.location.href = redirectUrl;
        }
    } else {
        alert("Now application in beta-test mode, so we support only telegram clients");
    }
});