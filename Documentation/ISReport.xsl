<?xsl version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
		<HTML>
			<HEAD>
				<TITLE>Instruction Set Command Report</TITLE>
			</HEAD>
			<BODY>
				<font face="Verdana">
					<table width="100%" border="2" cellpadding="3" cellspacing="0">
						<tr bgColor="gainsboro">
							<td align="center" colspan="2">
								<font size="4" face="Verdana">
									<b>Instruction Set Command Report</b>
								</font>
							</td>
						</tr>
						<tr>
							<td align="center" width="50%">
								<small><small>1.0.1.0</small></small>
							</td>
							<td align="center" width="50%">
								<small><small>Nov 29, 2006</small></small>
							</td>
						</tr>
					</table>
					<br/>
					Notes to evaluation:
					<ul>
						<li>Commands</li>
						<ul>
							<li>User Commands</li>
							<ul>
								<li>If a command is of type sys, the "GSIOC" will actually be a firmware specific instruction.</li>
								<li>All "Wait for" commands will  have no "GSIOC" entry.</li>
							</ul>
							<li>Status Commands</li>
							<ul>
								<li>Status is sent once per command or every cycle</li>
							</ul>
							<li>Motion Commands</li>
							<ul>
								<li>A motion command will cause all status commands to be sent</li>
								<li>A motion command is defined as a return parameter in the Get Motor Status command</li>
								<li>A command with motion commands will cause the motion commands to be run until the motion is complete</li>
							</ul>
						</ul>
						<li>Command Parameters</li>
						<ul>
							<li>If there are no entries under the Parameters, there are no parameters.</li>
							<li>Defaults are optional.</li>
							<li>Units are optional.</li>
							<li >
								<table border="0" cellpadding="0" cellspacing="0" >
									<tr>
										<td bgcolor="lightblue" >Command parameter headers are light blue</td>
									</tr>
								</table>
							</li>
							<li >
								<table border="0" cellpadding="0" cellspacing="0">
									<tr>
										<td bgcolor="salmon" valign="top">Return parameter headers are salmon.</td>
									</tr>
								</table>
							</li>
							<li >
								<table border="0" cellpadding="0" cellspacing="0">
									<tr>
										<td bgcolor="moccasin" valign="top">Motion command headers are moccasin.</td>
									</tr>
								</table>
							</li>
						</ul>
					</ul>
					
					<table border="0" cellpadding="1" cellspacing="2" width="100%">
						
						<xsl:for-each select="Gilson/InstructionSet/Devices/Device">
														
									<tr>
										<td bgcolor="#cccccc" valign="top" width="30%">
											<h2>Device Name</h2>
										</td>
									
										<td bgcolor="#cccccc" valign="top" width="70%">
											<h2><xsl:value-of select="DeviceName"/></h2>
										</td>
									</tr>
									<tr>
										<td bgcolor="#cccccc" valign="top">
											Version
										</td>
									
										<td bgcolor="#cccccc" valign="top">
											<xsl:value-of select="DeviceVersion"/>
										</td>
									</tr>
									<tr>
										<td bgcolor="#cccccc" valign="top">
											Unit ID
										</td>
									
										<td bgcolor="#cccccc" valign="top">
											<xsl:value-of select="DeviceId"/>
										</td>
									</tr>
									
									<!-- Add status information -->
									<xsl:if test="./StatusDefinition">
										<tr>
											<td colspan="2">
												<table border="1" cellpadding="1" cellspacing="2" width="100%">
													<tr>
														<td bgcolor="gainsboro" valign="top">
															<strong>Status Command</strong>
														</td>
														<td bgcolor="gainsboro" valign="top">
															<strong>Frequency</strong>
														</td>
													</tr>
													<xsl:for-each select="./StatusDefinition/StatusCommands/StatusCommand">
														<tr>
															<td bgcolor="white" valign="top">
																<small><xsl:value-of select="CommandName"/></small>
															</td>
																<xsl:choose>
																	<xsl:when test="PollingCommand = 0">
																		<td bgcolor="white" valign="top">
																			<small>Sent once per command</small>
																		</td>
																	</xsl:when>
																	<xsl:otherwise>
																		<td bgcolor="white" valign="top">
																			<small>Always on</small>
																		</td>
																	</xsl:otherwise>
																</xsl:choose>
														</tr>
													</xsl:for-each>
												</table>
											</td>
										</tr>
									</xsl:if>
									
									<!-- Add data collection information -->
									<xsl:if test="./DataDefinition">
										<tr>
											<td colspan="2">
												<table border="1" cellpadding="1" cellspacing="2" width="100%">
													<xsl:if test="./DataDefinition/EventQueueCommand">
														<tr>
															<td bgcolor="white" valign="top">
																<small>Event Queue Command</small>
															</td>
															<td bgcolor="white" valign="top">
																<small><xsl:value-of select="./DataDefinition/EventQueueCommand/CommandName"/></small>
															</td>
														</tr>
													</xsl:if>
													
													<tr>
														<td bgcolor="gainsboro" valign="top">
															<strong>Data Command</strong>
														</td>
														<td bgcolor="gainsboro" valign="top">
															<strong>Data Channel</strong>
														</td>
													</tr>

													<xsl:for-each select="./DataDefinition/DataCommand">
														<tr>
															<td bgcolor="white" valign="top">
																<small><xsl:value-of select="CommandName"/></small>
															</td>
															<td bgcolor="white" valign="top">
																<small><xsl:value-of select="Channel"/></small>
															</td>
														</tr>
													</xsl:for-each>
												</table>
											</td>
										</tr>
									</xsl:if>
									
									<tr>
										<td colspan="2">
											<table border="1" cellpadding="1" cellspacing="2" width="100%">
												<tr>
												
																<td bgcolor="gainsboro" valign="top">
																	<strong>Command Name</strong>
																</td>
																<td bgcolor="gainsboro" valign="top">
																	<strong>Notes</strong>
																</td>
																<td bgcolor="gainsboro" valign="top">
																	<strong>Parameters</strong>
																</td>
																
												</tr>
												
												
												<xsl:for-each select="./CommandDefinitions/CommandDefinition">
																				
															<tr>
															
																<td bgcolor="white" valign="top">
																	<xsl:value-of select="CommandName"/>
																</td>
																<td bgcolor="white" valign="top">
																	<small><xsl:value-of select="CommandNotes"/></small>
																</td>
																		<td>
																			<table border="0" cellpadding="1" cellspacing="2" width="100%">
																				<xsl:if test="./Parameters">
																					<tr>
																									<td width="30%"  bgcolor="lightblue" valign="top">
																										<small><u>Name</u></small>
																									</td>
																									<td width="15%" bgcolor="lightblue" valign="top">
																										<small><u>Type</u></small>
																									</td>
																									<td width="10%" bgcolor="lightblue" valign="top">
																										<small><u>Default</u></small>
																									</td>
																									<td width="10%" bgcolor="lightblue" valign="top">
																										<small><u>Units</u></small>
																									</td>
																									<td width="10%" bgcolor="lightblue" valign="top">
																										<small><u>Range</u></small>
																									</td>
																									<td width="25%" bgcolor="lightblue" valign="top">
																										<small><u>Notes</u></small>
																									</td>
																					</tr>
																					<xsl:for-each select="./Parameters/Parameter">
																												
																						<tr>
																							<td bgcolor="white" valign="top">
																								<small><xsl:value-of select="ParameterName"/></small>
																							</td>
																							<td bgcolor="white" valign="top">
																								<small><xsl:value-of select="ParameterType"/></small>
																							</td>	
																							<td bgcolor="white" valign="top">
																								<small><xsl:value-of select="ParameterDefault"/></small>
																							</td>	
																							<td bgcolor="white" valign="top">
																								<small><xsl:value-of select="ParameterUnits"/></small>
																							</td>	
																							<td bgcolor="white" valign="top">
																								<small><xsl:value-of select="RangeInfo/Min"/> - <xsl:value-of select="RangeInfo/Max"/></small>
																							</td>	
																							<td bgcolor="white" valign="top">
																								<small><xsl:value-of select="ParameterNotes"/></small>
																							</td>
																						</tr>			
																					</xsl:for-each>
																				</xsl:if>
																				
																				<xsl:if test="./ReturnParameters">
																					<tr>
																									<td width="30%"  bgcolor="salmon" valign="top">
																										<small><u>Name</u></small>
																									</td>
																									<td width="15%" bgcolor="salmon" valign="top">
																										<small><u>Type</u></small>
																									</td>
																									<td width="25%" bgcolor="salmon" valign="top" colspan="4">
																										<small><u>Notes</u></small>
																									</td>
																					</tr>
																					<xsl:for-each select="./ReturnParameters/ReturnParameter">
																														
																						<tr>
																							<td bgcolor="white" valign="top">
																								<small><xsl:value-of select="ParameterName"/></small>
																							</td>
																							<td bgcolor="white" valign="top">
																								<small><xsl:value-of select="ParameterType"/></small>
																							</td>	
																							<td bgcolor="white" valign="top" colspan="4">
																								<small><xsl:value-of select="ParameterNotes"/></small>
																							</td>
																						</tr>			
																					</xsl:for-each>
																				</xsl:if>
																				
																					<xsl:if test="./MotionCommands">
																					<tr>
																						<td width="30%"  bgcolor="moccasin" valign="top" colspan="6">
																							<small><u>Name</u></small>
																						</td>
																					</tr>
																					<xsl:for-each select="./MotionCommands/CommandName">
																														
																						<tr>
																							<td bgcolor="white" valign="top" colspan="6">
																								<small><xsl:value-of select="."/></small>
																							</td>
																						</tr>			
																					</xsl:for-each>
																				</xsl:if>
		
																			</table>
																		</td>
																</tr>			
												</xsl:for-each>
												
											</table>
										</td>
									</tr>									
						</xsl:for-each>
					</table>
					<br/>
					<small><small>Gilson Inc.</small></small>
				</font>
			</BODY>
		</HTML>
	</xsl:template>
</xsl:stylesheet>
