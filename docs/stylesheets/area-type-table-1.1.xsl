<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <xsl:template match="/">
        <html>
        <xsl:apply-templates/>
        </html>
    </xsl:template>

    <xsl:template match="area_type_table">
        <head>
        <!-- Put something useful into the Title -->
        <title>CF area types</title>
        </head>
        <body>
            <b>Version <xsl:value-of select="version_number"/>, <xsl:value-of select="date"/></b>
            <br/>
            <table id="area_type_table" border="1" width="100%" cellpadding="2" cellspacing="0">
                <th width="100%">Area Type</th>
                <xsl:apply-templates select="entry"/>
            </table>            
        </body>
    </xsl:template>

    <xsl:template match="entry">
        <tr>
            <xsl:attribute name="id"><xsl:value-of select="@id"/>_tr</xsl:attribute>
            
            <td>
                <a>
                    <xsl:attribute name="name">
                        <xsl:value-of select="@id"/>
                    </xsl:attribute>
                </a>
                <details>
                <summary>
                <code class="varname">
                    <xsl:value-of select="@id"/>
                </code>
                </summary>
                <xsl:variable name="area_type_id" select="@id"/>
                <xsl:apply-templates select="../alias[entry_id=$area_type_id]"/>
                
                <div>
                    <xsl:attribute name="id"><xsl:value-of select="@id"/>_help</xsl:attribute>
                    <xsl:attribute name="style">padding-left: 16px; margin-top: 4px; border-top: 1px dashed #cccccc;</xsl:attribute>
                    
                    <xsl:choose>
                        <xsl:when test="description=''">
                            No help available.
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="description"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </div>
                </details>
                
            </td>
        </tr>
    </xsl:template>
    
    <xsl:template match="alias">
        <div style="padding-left: 16px;"><i>alias:</i>&#160;<xsl:value-of select="@id"/></div>
    </xsl:template>
    
</xsl:stylesheet>
