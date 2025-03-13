// Create a class for the element
class TimeChart extends HTMLElement {
    static observedAttributes = ["data", "type", "options"];

    constructor() {
        // Always call super first in constructor
        super();
        this.attachShadow({mode:'open'});
        this.shadowRootDiv = document.createElement('div');
        this.canvas = document.createElement('canvas');
        this.shadowRootDiv.append(this.canvas);
        this.shadowRoot.appendChild(this.shadowRootDiv);
        this.chart = null;
    }

    init_chart() {
        const [data, options, type] = this.getInputs();
        const context = this.canvas.getContext('2d');
        console.log("render called");
        this.chart = new Chart(context, {
            type: type,
            data: data,
            options: options

        });
    }

    getInputs() {
        return [
            JSON.parse(this.getAttribute('data')),
            JSON.parse(this.getAttribute("options") ?? "{}"),
            this.getAttribute("type") ?? "line"
         ];
    }

    update(chart, key, val){
        if (key === "data"){
            // when only changing data we do not need to
            // fully recreate the chart so we just call update
            chart.data = JSON.parse(val);
            chart.update();
        } else {
            // otherwise if the type or options change we should
            // do a full recreate
            this.chart.destroy();
            this.chart = null;
            this.init_chart()
        }
    }

    connectedCallback() {
         this.init_chart();
    }
      
    attributeChangedCallback(name, oldValue, newValue) {
        if(this.chart){
            this.update(this.chart, name, newValue);
        }
    }
}

customElements.define("time-chart", TimeChart);
