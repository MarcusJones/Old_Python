<xsl:output method="text" />

<xsl:template match="/">
   <!-- starting point for root node -->
   <!-- put your header line for the CSV here -->
   <xsl:apply-templates select="my-names/row" />

<xsl:template match="row">
   <xsl:apply-templates select="field" />
   <!-- newline at end of each row -->
   <xsl:text>&#xa;</xsl:text>

<xsl:template match="field">
    <!-- each field -->
    <xsl:value-of select="." />


    <!-- only output comma separator if not at last field -->
    <xsl:if test="position() != last()">
        <xsl:text>,</xsl:text>
    </xsl:if>




