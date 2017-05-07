<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" indent="no"/>

<xsl:template match="EnergyPlus_XML">
<ROOT>
<!-- New line, and select all OBJECTS -->
<xsl:text>&#xa;</xsl:text>
<xsl:apply-templates select="OBJECT"/>
</ROOT>

</xsl:template>

<xsl:template match="OBJECT">
	<!-- Select NAME and newline -->
	<xsl:apply-templates select="NAME"/>
	<xsl:text>&#xa;</xsl:text>
	<!-- Then select ATTR and newline -->
	<xsl:apply-templates select="ATTR"/>
	<xsl:text>&#xa;</xsl:text>
</xsl:template>

<!-- Write the name and a comma -->
<xsl:template match="NAME"><xsl:value-of select="." />
	<xsl:text>,</xsl:text>
    <!-- Tab, !, and comment -->
    <xsl:text>&#9;</xsl:text>    
    <xsl:text>!</xsl:text>
    <xsl:value-of select="@Comment"/>
</xsl:template>

    
<!-- Add a tab, then attribute -->
<xsl:template match="ATTR"><xsl:text>&#9;</xsl:text><xsl:value-of select="." />
    
    <!-- Add either a comma or a semi colon -->
    <xsl:if test="position() != last()">
        <xsl:text>,</xsl:text>
    </xsl:if>
    <xsl:if test="position() = last()">
        <xsl:text>;</xsl:text>
    </xsl:if>
    
    <!-- Tab, !, and comment -->
    <xsl:text>&#9;</xsl:text>    
    <xsl:text>!</xsl:text>
    <xsl:value-of select="@Comment"/>
    
    <!-- New line -->
    <xsl:text>&#xa;</xsl:text>
</xsl:template>

</xsl:stylesheet>


