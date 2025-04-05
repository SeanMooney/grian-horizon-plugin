// Create a class for the element
class TimeChart extends HTMLElement {
    static observedAttributes = ["data", "data_ref", "type", "options"];

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
        this.chart = new Chart(context, {
            type: type,
            data: data,
            options: options

        });
    }

    getInputs() {
        let raw_data =  this.getAttribute('data');
        let data_ref =  this.getAttribute('data_ref');
        if (data_ref){
            let external_data_ref = htmx.find(data_ref);
            raw_data = external_data_ref.innerHTML;
        }
        return [
            JSON.parse(raw_data),
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
    
    external_data_callback(mutationList, observer){
        for (const mutation of mutationList) {
            if(mutation.addedNodes.length > 0) {
                const added = mutation.addedNodes[0].data;
                this.update(this.chart, "data", added);
            }
        }
    }

    connectedCallback() {
        let raw_data =  this.getAttribute('data');
        let data_ref =  this.getAttribute('data_ref');
        if (raw_data && data_ref) {
            throw new Error("Only one of data or data_ref can be specified");
        } else if (!raw_data && !data_ref){
            throw new Error("one of data or data_ref must be specified");
        }
        
        if (data_ref){
            const mutation_observer = new MutationObserver(
                (mutationList, observer) => this.external_data_callback(mutationList, observer));
            const config = {childList: true, subtree: true };
            const targetNode = document.querySelector(data_ref);
            mutation_observer.observe(targetNode,config);
        }
        this.init_chart();
    }
      
    attributeChangedCallback(name, oldValue, newValue) {
        if(this.chart){
            this.update(this.chart, name, newValue);
        }
    }
}

customElements.define("time-chart", TimeChart);
