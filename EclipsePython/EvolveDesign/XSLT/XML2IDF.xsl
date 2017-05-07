<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">>
<xsl:output method="text"/><xsl:template match="/">
<xsl:text>id,name,price,stock,country</xsl:text>
<xsl:for-each select="products/product">
<xsl:value-of select="@id"/>
<xsl:text>,</xsl:text>
<xsl:value-of select="name"/>
<xsl:text>,</xsl:text>
<xsl:value-of select="price"/>
<xsl:text>,</xsl:text>
<xsl:value-of select="stock"/>
<xsl:text>,</xsl:text>
<xsl:value-of select="country"/>
<xsl:text>
</xsl:text>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>