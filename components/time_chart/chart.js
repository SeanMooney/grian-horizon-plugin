// Create a class for the element
class TimeChart extends HTMLElement {
    static observedAttributes = ["data", "type"];

    constructor() {
        // Always call super first in constructor
        super();
    }

    connectedCallback() {
        const data = this.getAttribute("data");
        const type = this.getAttribute("renderer") ?? "line";
        const width = this.getAttribute("width") ?? 400;
        const height = this.getAttribute("height") ?? 400;
        const style = this.getAttribute("style") ?? "";
        const stacked = this.getAttribute("stacked") || false;
        const stroke = this.getAttribute("stroke") ?? false;
    
        const shadow = this.attachShadow({ mode: "open" });
        
        
        const inner_style = document.createElement("style");
        inner_style.textContent = style;
        shadow.appendChild(inner_style);

        const wrapper = document.createElement("div");
        
        shadow.appendChild(wrapper);


        const graph = new Rickshaw.Graph({
            padding: { top: 0.025, right: 0.025, bottom: 0.025, left: 0.025 },
            min: "0",
            stack: false,
            width: width,
            height: height,
            element: wrapper,
            renderer: type,
            series: JSON.parse(data)
        });
        
        graph.render();

        
    }

    disconnectedCallback() {
        console.log("Custom element removed from page.");
    }

    adoptedCallback() {
        console.log("Custom element moved to new page.");
    }

    attributeChangedCallback(name, oldValue, newValue) {
        console.log(`Attribute ${name} has changed.`);
    }
}

customElements.define("time-chart", TimeChart);
