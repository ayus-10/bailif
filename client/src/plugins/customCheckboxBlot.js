import { Quill } from "@vueup/vue-quill";

const Embed = Quill.import("blots/embed");

export class CustomCheckboxBlot extends Embed {
    static blotName = "customCheckbox";
    static tagName = "span";
    static className = "ql-custom-checkbox";

    // Runs whenever this embed is inserted OR when Quill renders a delta
    // that contains one (e.g. loading saved content) — builds the DOM.
    static create(value) {
        const node = super.create(value);
        node.setAttribute("contenteditable", "false");
        node.setAttribute("data-id", value.id);
        node.setAttribute("data-checked", String(!!value.checked));

        const box = document.createElement("input");
        box.type = "checkbox";
        box.checked = !!value.checked;
        // Prevent the click from doing weird things to Quill's selection
        box.addEventListener("mousedown", (e) => e.stopPropagation());
        box.addEventListener("change", () => {
            node.setAttribute("data-checked", String(box.checked));
            // Bubble a plain DOM event — the Vue layer listens for this and
            // updates whatever app state / store actually owns the task list.
            node.dispatchEvent(
                new CustomEvent("checkbox-toggle", {
                    bubbles: true,
                    detail: { id: value.id, checked: box.checked },
                })
            );
        });

        const label = document.createElement("span");
        label.className = "ql-custom-checkbox-label";
        label.textContent = value.label ?? "";

        node.appendChild(box);
        node.appendChild(label);
        return node;
    }

    // Runs whenever Quill needs to turn this DOM node back into delta data
    // (on save, on diff, on undo/redo). Keep it a plain serializable object.
    static value(node) {
        return {
            id: node.getAttribute("data-id"),
            checked: node.getAttribute("data-checked") === "true",
            label:
                node.querySelector(".ql-custom-checkbox-label")?.textContent ??
                "",
        };
    }
}

Quill.register(CustomCheckboxBlot);
