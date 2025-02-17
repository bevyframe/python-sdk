const renderWidget = (data, parent = document.body) => {
    if (Array.isArray(data) && data.length === 3) {
        const [tag, attrs, children] = data;
        const el = document.createElement(tag);
        Object.entries(attrs || {}).forEach(([key, value]) => {
            el.setAttribute(key, value);
        });
        children.forEach(child => {
            if (Array.isArray(child)) {
                renderWidget(child, el);
            } else {
                el.appendChild(document.createTextNode(child));
            }
        });
        parent.appendChild(el);
    } else {
        parent.innerHTML = parent.innerHTML + data;
    }
}

const renderAll = () => {
    document.body.innerHTML = "";
    for (let element of `---body---`) {
        renderWidget(element);
    }
};