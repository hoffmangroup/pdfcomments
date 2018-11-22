<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xfdf="http://ns.adobe.com/xfdf/"
                xmlns:str="http://exslt.org/strings"
                extension-element-prefixes="str"
                version="1.0">

  <xsl:output method="text" />

  <!-- https://www.oreilly.com/library/view/xslt-cookbook/0596003722/ch01s07.html -->
  <xsl:template name="search-and-replace">
    <xsl:param name="input"/>
    <xsl:param name="search-string"/>
    <xsl:param name="replace-string"/>
    <xsl:choose>
      <!-- See if the input contains the search string -->
      <xsl:when test="$search-string and 
                      contains($input,$search-string)">
                      <!-- If so, then concatenate the substring before the search
                           string to the replacement string and to the result of
                           recursively applying this template to the remaining substring.
                      -->
                      <xsl:value-of 
                          select="substring-before($input,$search-string)"/>
                      <xsl:value-of select="$replace-string"/>
                      <xsl:call-template name="search-and-replace">
                        <xsl:with-param name="input"
                                        select="substring-after($input,$search-string)"/>
                        <xsl:with-param name="search-string" 
                                        select="$search-string"/>
                        <xsl:with-param name="replace-string" 
                                        select="$replace-string"/>
                      </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <!-- There are no more occurences of the search string so 
             just return the current input string -->
        <xsl:value-of select="$input"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
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
