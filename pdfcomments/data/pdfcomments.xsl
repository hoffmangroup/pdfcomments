<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xfdf="http://ns.adobe.com/xfdf/"
                xmlns:str="http://exslt.org/strings"
                extension-element-prefixes="str"
                version="1.0">

  <xsl:output method="text" />

  <xsl:template match="xfdf:xfdf">
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="xfdf:ink">p<xsl:value-of select="@page+1" />: [ink]<xsl:text>
</xsl:text></xsl:template>
  
  <xsl:template match="xfdf:freetext">p<xsl:value-of select="@page+1" />: <xsl:apply-templates /><xsl:text>
</xsl:text>
  </xsl:template>

  <xsl:template match="xfdf:defaultappearance" />
  <xsl:template match="xfdf:defaultstyle" />

</xsl:stylesheet>
