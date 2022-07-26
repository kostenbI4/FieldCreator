header = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Created with Jaspersoft Studio version 6.17.0.final using JasperReports Library version 6.17.0-6d93193241dd8cc42629e188b94f9e0bc5722efd  -->
<jasperReport xmlns="http://jasperreports.sourceforge.net/jasperreports" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://jasperreports.sourceforge.net/jasperreports http://jasperreports.sourceforge.net/xsd/jasperreport.xsd" name="{name}" pageWidth="1684" pageHeight="1191" orientation="Landscape" whenNoDataType="AllSectionsNoDetail" columnWidth="1644" leftMargin="20" rightMargin="20" topMargin="20" bottomMargin="20" uuid="717c634f-d51d-4c31-9ceb-77f32ebbd09e">
	<property name="com.jaspersoft.studio.data.defaultdataadapter" value="One Empty Record"/>
	<property name="net.sf.jasperreports.export.xls.detect.cell.type" value="true"/>
	<property name="net.sf.jasperreports.export.docx.frames.as.nested.tables" value="false"/>
	<template><![CDATA["reports/style.jrtx"]]></template>
	<parameter name="HEAD" class="java.lang.String"/>
	<queryString>
		<![CDATA[]]>
	</queryString>
"""

titleHead = """
        <band height="146" splitType="Stretch">
			<property name="com.jaspersoft.studio.layout" value="com.jaspersoft.studio.editor.layout.grid.JSSGridBagLayout"/>
			<textField textAdjust="StretchHeight" isBlankWhenNull="true">
				<reportElement style="title" stretchType="ContainerHeight" mode="Transparent" x="0" y="0" width="1644" height="98" uuid="fe025375-b976-47db-98bb-fd880b83076e">
					<property name="com.jaspersoft.layout.grid.x" value="-1"/>
					<property name="com.jaspersoft.layout.grid.y" value="0"/>
					<property name="com.jaspersoft.layout.grid.weight.x" value="1.0"/>
					<property name="com.jaspersoft.layout.grid.weight.y" value="2.0"/>
					<property name="com.jaspersoft.layout.grid.rowspan" value="1"/>
					<property name="com.jaspersoft.layout.grid.colspan" value="18"/>
					<property name="com.jaspersoft.layout.grid.weight.fixed" value="false"/>
				</reportElement>
				<textElement textAlignment="Center" verticalAlignment="Middle"/>
				<textFieldExpression><![CDATA[$P{HEAD}]]></textFieldExpression>
			</textField>"""

fildName = """
            <staticText>
				<reportElement style="header" x="{coord}" y="98" width="{width}" height="48" uuid="76e7c0fd-f74e-4148-badc-f0b3cab83ba6">
					<property name="com.jaspersoft.layout.grid.x" value="-1"/>
					<property name="com.jaspersoft.layout.grid.y" value="1"/>
					<property name="com.jaspersoft.layout.grid.weight.x" value="1.0"/>
					<property name="com.jaspersoft.layout.grid.weight.y" value="1.0"/>
					<property name="com.jaspersoft.layout.grid.rowspan" value="2"/>
					<property name="com.jaspersoft.layout.grid.colspan" value="1"/>
					<property name="com.jaspersoft.layout.grid.weight.fixed" value="false"/>
				</reportElement>
				<box>
					<pen lineWidth="0.5"/>
				</box>
				<text><![CDATA[{name}]]></text>
			</staticText>
"""

columnHeaderFirstField = """
            <staticText>
				<reportElement style="header" x="{coord}" y="0" width="{width}" height="24" uuid="e72cc33e-72ee-42a1-8256-1b8bcefc14ca">
					<property name="com.jaspersoft.layout.grid.x" value="-1"/>
					<property name="com.jaspersoft.layout.grid.y" value="0"/>
					<property name="com.jaspersoft.layout.grid.weight.x" value="1.0"/>
					<property name="com.jaspersoft.layout.grid.weight.y" value="1.0"/>
					<property name="com.jaspersoft.layout.grid.rowspan" value="1"/>
					<property name="com.jaspersoft.layout.grid.colspan" value="1"/>
					<property name="com.jaspersoft.layout.grid.weight.fixed" value="false"/>
					<property name="net.sf.jasperreports.export.xls.freeze.row.edge" value="Bottom"/>
				</reportElement>
				<box>
					<pen lineWidth="0.5"/>
				</box>
				<textElement textAlignment="Center" verticalAlignment="Middle"/>
				<text><![CDATA[{count}]]></text>
			</staticText>
"""

columnHeaderField = """
            <staticText>
				<reportElement style="header" x="{coord}" y="0" width="{width}" height="24" uuid="e72cc33e-72ee-42a1-8256-1b8bcefc14ca">
					<property name="com.jaspersoft.layout.grid.x" value="-1"/>
					<property name="com.jaspersoft.layout.grid.y" value="0"/>
					<property name="com.jaspersoft.layout.grid.weight.x" value="1.0"/>
					<property name="com.jaspersoft.layout.grid.weight.y" value="1.0"/>
					<property name="com.jaspersoft.layout.grid.rowspan" value="1"/>
					<property name="com.jaspersoft.layout.grid.colspan" value="1"/>
					<property name="com.jaspersoft.layout.grid.weight.fixed" value="false"/>
				</reportElement>
				<box>
					<pen lineWidth="0.5"/>
				</box>
				<textElement textAlignment="Center" verticalAlignment="Middle"/>
				<text><![CDATA[{count}]]></text>
			</staticText>
"""

columnHeader = """
<columnHeader>
		<band height="24">
			<property name="com.jaspersoft.studio.layout" value="com.jaspersoft.studio.editor.layout.grid.JSSGridBagLayout"/>
			<property name="com.jaspersoft.studio.unit.height" value="px"/>
			{data}
        </band>
</columnHeader>
"""

detail = """
    <detail>
        <band height="95">
            <property name="com.jaspersoft.studio.layout" value="com.jaspersoft.studio.editor.layout.grid.JSSGridBagLayout"/>
            <property name="com.jaspersoft.studio.unit.height" value="pixel"/>
            {data}
        </band>
    </detail>
"""

detailTextField = """
            <textField textAdjust="StretchHeight">
                    <reportElement style="cell" stretchType="ContainerHeight" x="{coord}" y="0" width="{width}" height="95" uuid="6836266a-dc95-48c3-9d06-cf4fec37082e">
                        <property name="net.sf.jasperreports.export.xls.auto.fit.row" value="true"/>
                        <property name="com.jaspersoft.layout.grid.x" value="-1"/>
                        <property name="com.jaspersoft.layout.grid.y" value="-1"/>
                        <property name="com.jaspersoft.layout.grid.weight.x" value="1.0"/>
                        <property name="com.jaspersoft.layout.grid.weight.y" value="1.0"/>
                        <property name="com.jaspersoft.layout.grid.rowspan" value="1"/>
                        <property name="com.jaspersoft.layout.grid.colspan" value="1"/>
                        <property name="com.jaspersoft.layout.grid.weight.fixed" value="false"/>
                        <property name="net.sf.jasperreports.style.pattern" value="{pattern}"/>
                        <property name="net.sf.jasperreports.export.xls.pattern" value="{pattern}"/>
                        <property name="net.sf.jasperreports.style.isBlankWhenNull" value="true"/>
                    </reportElement>
                    <box>
                        <pen lineWidth="0.5"/>
                    </box>
                    <textFieldExpression><![CDATA[{name}]]></textFieldExpression>
            </textField>
"""

variable = """
    <variable name="{name}" class="java.time.format.DateTimeFormatter">
		<variableExpression><![CDATA[java.time.format.DateTimeFormatter.ofPattern("{pattern}")]]></variableExpression>
	</variable>
"""

testData = """
    //Бизнес-процесс
    @Column(name = "swcmnemocode")
    private String wcMnemocode;

    //Наименование
    @Column(name = "scaption")
    private String caption;

    //Модель
    @Column(name = "smnemocode")
    private String mnemoCode;

    //Инвентарный номер
    @Column(name = "sinventorynum")
    private String inventoryNum;

    //Координаты
    @Column(name = "scoordloc")
    private String coordLoc;

    //Профиль
    @Column(name = "sprofile")
    private String profile;

    //К раб дней
    @Column(name = "sdays")
    private String days;

    //К смен в сутки
    @Column(name = "nshifts")
    private Integer shifts;

    //Количество рабочих часов
    @Column(name = "fduration")
    private Double duration;

    //Номер смены
    @Column(name = "nshift")
    private Integer shift;

    //Время начала
    @Column(name = "tbegin")
    private LocalTime begin;

    //Время окончания
    @Column(name = "tend")
    private LocalTime end;

    //Исключения к календарю профиля (
    @Column(name = "sclndexception")
    private String clndException;

    //Индикатор строки итога
    @Column(name = "bitog")
    private Integer itog;"""
