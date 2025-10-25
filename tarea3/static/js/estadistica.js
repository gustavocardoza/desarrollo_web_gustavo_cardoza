// Grafico 1
Highcharts.chart('container1', {
    chart: {
        type: 'line'
    },
    title: {
        text: 'Cantidad de Avisos de Adopción por Día'
    },
    xAxis: {
        type: "datetime",
        dateTimeLabelFormats: {
            month: "%b %e, %Y",
        },
        title: {
            text: "Fecha",
        },
    },
    yAxis: {
        title: {
            text: 'Cantidad de Avisos'
        }
    },
    series: [{
        name: 'Avisos de Adopción',
        data: []
    }]
});

// Grafico 2
Highcharts.chart('container2', {
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Total de Avisos de Adopción por Tipo de Mascota'
    },
    series: [{
        name: 'Mascotas',
        data: [
            { name: 'Perros', y: 0 }, 
            { name: 'Gatos', y: 0 }  
        ],
        showInLegend: true,
        dataLabels: {
            enabled: true,
            format: '{point.name}: {point.percentage:.1f} %'
        }
    }],
    tooltip: {
        pointFormat: '<b>{point.y}</b> avisos ({point.percentage:.1f} %)'
    }
});

// Grafico 3
Highcharts.chart('container3', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Avisos de Adopción de Gatos y Perros por Mes'
    },
    xAxis: {
        type: "datetime",
        dateTimeLabelFormats: {
            month: "%b %Y",
        },
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Cantidad de Avisos'
        }
    },
    series: [{
        name: 'Gatos',
        data: [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
    }, {
        name: 'Perros',
        data: [12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78]
    }],
    tooltip: {
        shared: true,
        valueSuffix: ' avisos'
    }
});

// Fetch
fetch("http://127.0.0.1:5000/get-stats-data")
    .then((response) => response.json()) // json -> js
    .then(data => {
        console.log(data);
        // 1er grafico
        const data_grafico1 = data.data_avisos_diarios;
        let parsedData = data_grafico1.map((item)=>{
            const [anho, mes, dia] = item.fecha.split("-").map((part) => parseInt(part, 10));
            return [
                Date.UTC(anho, mes-1, dia), item.cantidad
            ];
        });

        const chart1 = Highcharts.charts.find(
        (chart) => chart && chart.renderTo.id === "container1"
        );

        chart1.update({
            series: [
                {
                    data: parsedData,
                },
            ],
        });
        
        // 2do gráfico
        const data_grafico2 = data.data_total_perros_gatos[0];
        const chart2 = Highcharts.charts.find(
        (chart) => chart && chart.renderTo.id === "container2"
        );
        
        chart2.update({
            series: [{
                name: 'Mascotas',
                data: [
                    { name: 'Perros', y: parseInt(data_grafico2.cantidad_total_perros) }, 
                    { name: 'Gatos', y: parseInt(data_grafico2.cantidad_total_gatos) }
                ],
                showInLegend: true,
                dataLabels: {
                    enabled: true,
                    format: '{point.name}: {point.percentage:.1f} %'
                }
            }],
        });

        // 3er gráfico
        const data_grafico3 = data.data_perros_gatos_mensual;
        const chart3 = Highcharts.charts.find(
        (chart) => chart && chart.renderTo.id === "container3"
        );
        
        // Decidí que solo se vieran de los últimos doce meses
        const hoy = new Date();
        const hace_12_meses = new Date();
        hace_12_meses.setMonth(hoy.getMonth() - 12);

        // Se filtran los datos
        const datos_filtrados = data_grafico3.filter((item) => {
            const fechaDato = new Date(item.fecha);
            return fechaDato >= hace_12_meses;
        });

        let parsedPerros = datos_filtrados.map((item)=>{
            const [anho, mes] = item.fecha.split("-").map((part) => parseInt(part, 10));
            return [
                Date.UTC(anho, mes-1), parseInt(item.cantidad_perros)
            ];
        });

        let parsedGatos = datos_filtrados.map((item)=>{
            const [anho, mes] = item.fecha.split("-").map((part) => parseInt(part, 10));
            return [
                Date.UTC(anho, mes-1), parseInt(item.cantidad_gatos)
            ];
        });

        chart3.update({
            series: [{
                name: 'Gatos',
                data: parsedGatos
            }, {
                name: 'Perros',
                data: parsedPerros
            }],
            tooltip: {
                shared: true,
                valueSuffix: 'avisos'
            }
        })

    })
    .catch((error) => console.error("Error:", error))